"""Prepare and validate the repository HTML and the exported Pages site."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote


REPOSITORY = Path(__file__).resolve().parents[2]
SITE_URL = "https://mamedov-anar.github.io/dr.derekk/"
TREATMENTS_URL = SITE_URL + "treatments/"
CARD_PATH = re.compile(r"treatments/[^/]+/index\.html")
METRIKA_ID = "114682237"
START = "<!-- Yandex.Metrika counter -->"
END = "<!-- /Yandex.Metrika counter -->"
FALLBACK = "metrika-404-fallback"
INIT = re.compile(r"""\bym\s*\(\s*(\d+)\s*,\s*['"]init['"]\s*,\s*\{([^{}]*)\}\s*\)""")
INIT_OPTIONS = {
    "ssr:true", "webvisor:true", "clickmap:true", "referrer:document.referrer",
    "url:location.href", "accurateTrackBounce:true", "trackLinks:true",
}
COUNTER_MARK = re.compile(
    r"""<!--\s*/?\s*Yandex\.Metrika counter\b|[/]metrika/(?:tag[^/?\s]*|watch)\.js\b"""
    r"""|mc\.yandex\.[\w.]+/watch\b|\bym\s*\([^,]+,\s*['"]init['"]|\bYa\.Metrika2?\s*\(""",
    re.IGNORECASE,
)


class BodyStart(HTMLParser):
    def __init__(self):
        super().__init__()
        self.position = None

    def handle_starttag(self, tag, attrs):
        if tag == "body" and self.position is None:
            self.position = (*self.getpos(), len(self.get_starttag_text()))


def body_end(html):
    parser = BodyStart()
    parser.feed(html)
    parser.close()
    if parser.position is None:
        raise ValueError("missing opening <body> tag")
    line, column, tag_length = parser.position
    return html_offset(html, line, column) + tag_length


def html_offset(html, line, column):
    return len(html) - len(html.split("\n", line - 1)[-1]) + column


class PageMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.head_end = None
        self.canonicals = []
        self.headings = set()
        self.heading = None
        self.script = None
        self.breadcrumbs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
        elif tag == "link" and self.in_head and "canonical" in (attrs.get("rel") or "").lower().split():
            self.canonicals.append((attrs.get("href") or "").strip())
        elif tag == "h1":
            self.heading = []
        elif tag == "br" and self.heading is not None:
            self.heading.append(" ")
        elif tag == "script" and (attrs.get("type") or "").strip().lower() == "application/ld+json":
            self.script = []

    def handle_data(self, data):
        if self.script is not None:
            self.script.append(data)
        elif self.heading is not None:
            self.heading.append(data)

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
            self.head_end = self.getpos()
        elif tag == "h1" and self.heading is not None:
            self.headings.add(" ".join("".join(self.heading).replace("\u00ad", "").split()))
            self.heading = None
        elif tag == "script" and self.script is not None:
            source = "".join(self.script)
            self.script = None
            try:
                data = json.loads(source)
            except json.JSONDecodeError as error:
                if "BreadcrumbList" in source:
                    raise ValueError("invalid BreadcrumbList JSON-LD") from error
            else:
                self.breadcrumbs.extend((self.in_head, entry) for entry in breadcrumb_lists(data))


def breadcrumb_lists(data):
    if isinstance(data, dict):
        kind = data.get("@type")
        if kind == "BreadcrumbList" or isinstance(kind, list) and "BreadcrumbList" in kind:
            yield data
        for value in data.values():
            yield from breadcrumb_lists(value)
    elif isinstance(data, list):
        for value in data:
            yield from breadcrumb_lists(value)


def prepare_breadcrumbs(html, name, check):
    page = PageMarkup()
    page.feed(html)
    page.close()
    expected_url = SITE_URL + quote(name.removesuffix("index.html"))
    if not CARD_PATH.fullmatch(name) or expected_url not in page.canonicals:
        if page.breadcrumbs:
            raise ValueError("BreadcrumbList found outside a canonical treatment page")
        return html, False
    if page.canonicals != [expected_url] or page.head_end is None:
        raise ValueError("expected one canonical URL and a closing </head> tag")
    if len(page.headings) != 1 or "" in page.headings:
        raise ValueError("expected one distinct non-empty treatment h1")

    title, = page.headings
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "item": {"name": "Процедуры", "@id": TREATMENTS_URL}},
            {"@type": "ListItem", "position": 2, "item": {"name": title, "@id": page.canonicals[0]}},
        ],
    }
    if page.breadcrumbs:
        if json.dumps(page.breadcrumbs, sort_keys=True) == json.dumps([(True, data)], sort_keys=True):
            return html, True
        raise ValueError("expected exactly one matching BreadcrumbList in <head>")
    if check:
        raise ValueError("missing BreadcrumbList in <head>")

    end = html_offset(html, *page.head_end)
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return f'{html[:end]}<script type="application/ld+json">{payload}</script>\n{html[end:]}', True


def metrika_blocks():
    source = Path(__file__).with_name("metrika.html.inc").read_text(encoding="utf-8").strip()
    counter, end, _ = source.partition(END)
    tag_url = f"https://mc.yandex.ru/metrika/tag.js?id={METRIKA_ID}"
    pixel_url = f"https://mc.yandex.ru/watch/{METRIKA_ID}"
    pixel = f'<noscript><div><img src="{pixel_url}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>'
    init = INIT.findall(source)
    if len(init) != 1 or init[0][0] != METRIKA_ID:
        raise ValueError(f"metrika.html.inc must initialize counter {METRIKA_ID} exactly once")
    options = re.sub(r"\s+", "", init[0][1]).split(",")
    if len(options) != len(INIT_OPTIONS) or set(options) != INIT_OPTIONS:
        raise ValueError("metrika.html.inc has unexpected init options")
    if (
        not end or not source.startswith(START) or source.count(tag_url) != 1
        or source.count(pixel_url) != 1 or pixel not in counter
        or len(COUNTER_MARK.findall(source)) != 5  # Two comments, loader, init and pixel.
    ):
        raise ValueError("metrika.html.inc must contain one loader and one noscript pixel")
    fallback = counter.replace(
        '<script type="text/javascript">', f'<template id="{FALLBACK}">\n<script type="text/javascript">', 1
    ).replace("</script>", "</script>\n</template>", 1)
    if f'<template id="{FALLBACK}">' not in fallback:
        raise ValueError("metrika.html.inc is missing the script for the 404 fallback")
    return source, fallback + end


def published_html(root):
    for directory, subdirectories, names in os.walk(root):
        if Path(directory) == root:
            subdirectories[:] = sorted(set(subdirectories) - {".git", ".github"})
            # Preserve the original verification HTML for Yandex Webmaster.
            names = [name for name in names if name != "yandex_ddb1b2810149db7c.html"]
        else:
            subdirectories.sort()
        for name in sorted(names):
            if Path(name).suffix.lower() in {".html", ".htm"}:
                yield Path(directory) / name


def prepare_html(html, expected, check):
    end = body_end(html)
    after_body = html[end:].lstrip()
    if after_body.startswith(expected):
        if COUNTER_MARK.search(html[:end]) or COUNTER_MARK.search(after_body[len(expected):]):
            raise ValueError("another Metrika connection found")
        return html
    if COUNTER_MARK.search(html):
        raise ValueError("misplaced, altered or duplicate Metrika code. Restore the generated block")
    if check:
        raise ValueError("missing Metrika code. Run python3 .github/pages/prepare.py")
    rest = html[end:].lstrip("\r\n")
    return f"{html[:end]}\n{expected}\n{rest}"


def update_manifests(root, names, check=False):
    manifest_path = root / "asset-manifest.json"
    sums_path = root / "SHA256SUMS.txt"
    manifest = json.loads(manifest_path.read_bytes())
    files = []
    for name in sorted(set(names) - {"", manifest_path.name, sums_path.name}):
        contents = (root / name).read_bytes()
        files.append({"path": name, "bytes": len(contents), "sha256": hashlib.sha256(contents).hexdigest()})
    manifest["files"] = files
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    checksums = {entry["path"]: entry["sha256"] for entry in files}
    checksums[manifest_path.name] = hashlib.sha256(manifest_bytes).hexdigest()
    sums_bytes = "".join(f"{sha}  {name}\n" for name, sha in sorted(checksums.items())).encode()
    for path, contents in ((manifest_path, manifest_bytes), (sums_path, sums_bytes)):
        if check:
            if path.read_bytes() != contents:
                raise ValueError(f"{path.name} does not match the exported site")
        else:
            path.write_bytes(contents)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--check", action="store_true", help="Report errors without changing files")
    cli.add_argument("--root", type=Path, help="Prepare or check this exported Pages directory")
    args = cli.parse_args()
    root = args.root.resolve() if args.root else REPOSITORY
    if args.root and root == REPOSITORY:
        cli.error("--root must point to a separate Pages export")
    check_metrika = args.check or args.root is not None
    standard, fallback = metrika_blocks()
    filenames = list(published_html(root))
    if not filenames:
        cli.error(f"no HTML documents found in {root}")

    errors = []
    changes = []
    treatment_count = 0
    for path in filenames:
        name = path.relative_to(root).as_posix()
        html = path.read_bytes().decode("utf-8")
        try:
            prepared = prepare_html(html, fallback if name == "404.html" else standard, check_metrika)
            if args.root:
                prepared, is_treatment = prepare_breadcrumbs(prepared, name, args.check)
                treatment_count += is_treatment
            if prepared != html:
                changes.append((path, prepared))
        except ValueError as error:
            errors.append(f"{name}: {error}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if not args.check:
        for path, prepared in changes:
            path.write_bytes(prepared.encode("utf-8"))

    if args.root:
        names = (path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
        try:
            update_manifests(root, names, args.check)
        except (OSError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1
        action = "Checked" if args.check else "Prepared"
        print(f"{action} BreadcrumbList for {treatment_count} canonical treatment pages.")
    elif not args.check:
        names = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=REPOSITORY
        ).decode().split("\0")
        update_manifests(root, names)
        print(f"Updated {len(changes)} HTML files and refreshed the manifests.")
    print(f"Checked {len(filenames)} HTML files for Metrika {METRIKA_ID}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
