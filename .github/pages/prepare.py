"""Prepare checked-in HTML and its manifests, or validate a Pages artifact."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
import sys


REPOSITORY = Path(__file__).resolve().parents[2]
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
    return len(html) - len(html.split("\n", line - 1)[-1]) + column + tag_length


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


def update_manifests():
    manifest_path = REPOSITORY / "asset-manifest.json"
    sums_path = REPOSITORY / "SHA256SUMS.txt"
    manifest = json.loads(manifest_path.read_bytes())
    names = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=REPOSITORY
    ).decode().split("\0")
    files = []
    for name in sorted(set(names) - {"", manifest_path.name, sums_path.name}):
        contents = (REPOSITORY / name).read_bytes()
        files.append({"path": name, "bytes": len(contents), "sha256": hashlib.sha256(contents).hexdigest()})
    manifest["files"] = files
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    manifest_path.write_bytes(manifest_bytes)
    checksums = {entry["path"]: entry["sha256"] for entry in files}
    checksums[manifest_path.name] = hashlib.sha256(manifest_bytes).hexdigest()
    sums_path.write_bytes("".join(f"{sha}  {name}\n" for name, sha in sorted(checksums.items())).encode())


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--check", action="store_true", help="Report errors without changing files")
    cli.add_argument("--root", type=Path, help="Check this exported Pages directory")
    args = cli.parse_args()
    if args.root and not args.check:
        cli.error("--root requires --check")
    root = args.root.resolve() if args.root else REPOSITORY
    standard, fallback = metrika_blocks()
    filenames = list(published_html(root))
    if not filenames:
        cli.error(f"no HTML documents found in {root}")

    errors = []
    changes = []
    for path in filenames:
        name = path.relative_to(root).as_posix()
        html = path.read_bytes().decode("utf-8")
        try:
            prepared = prepare_html(html, fallback if name == "404.html" else standard, args.check)
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
        update_manifests()
        print(f"Updated {len(changes)} HTML files and refreshed the manifests.")
    print(f"Checked {len(filenames)} HTML files for Metrika {METRIKA_ID}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
