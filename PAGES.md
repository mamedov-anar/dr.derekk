# Dr.Derek — справочник страниц

Состав страниц проверен **2 ноября 2026 года** по ветке `main` репозитория [mamedov-anar/dr.derekk](https://github.com/mamedov-anar/dr.derekk) и истории её коммитов. Срез перед добавлением справочника: [`3bc4cae`](https://github.com/mamedov-anar/dr.derekk/commit/3bc4cae5606b80b4aced295b6bd22780075a8976).

Публичный сайт: [mamedov-anar.github.io/dr.derekk/](https://mamedov-anar.github.io/dr.derekk/). Все адреса в таблицах указаны относительно этого сайта.

## Быстрый ориентир

- **Основной действующий каталог:** [`/treatments/`](https://mamedov-anar.github.io/dr.derekk/treatments/).
- **Точная копия действующего каталога:** [`/treatments_2/`](https://mamedov-anar.github.io/dr.derekk/treatments_2/). HTML полностью совпадает с `/treatments/`; копия опубликована отдельно для дальнейшей работы.
- **Новая тестовая страница услуг:** [`/services-preview/`](https://mamedov-anar.github.io/dr.derekk/services-preview/). Используется для просмотра и обсуждения структуры; основной каталог ею пока не заменён.
- **Основные страницы сайта:** главная, о враче, контакты, действующий каталог процедур.
- **Остальные действующие страницы:** 14 отдельных процедур, политика конфиденциальности и служебная страница 404.

## Категории и количество

| Категория | Количество | Статус |
| --- | ---: | --- |
| Основные страницы | 4 | Действующие, нетестовые |
| Внутренние страницы отдельных процедур | 14 | Действующие, нетестовые; раскрывают карточки основного каталога |
| Правовая страница | 1 | Действующая, нетестовая; вспомогательная |
| Тестовые страницы | 2 | Копия действующего каталога и новая структура услуг; не заменяют основной каталог |
| Служебная страница ошибки | 1 | Действующая, нетестовая; техническая |
| **Всего текущих страниц с отдельными маршрутами** | **22** | **20 исходных маршрутов + 2 тестовых** |

Дополнительно в корне есть технический файл `404.html`. Он обслуживает неизвестные адреса GitHub Pages и направляет посетителя на `/404/`. Это отдельный HTML-файл, но не самостоятельный раздел сайта. Всего в текущем дереве репозитория **23 HTML-файла**.

## 1. Основные страницы — действующие, нетестовые

| Страница | Адрес на сайте | Файл в репозитории | Назначение |
| --- | --- | --- | --- |
| Главная | [`/`](https://mamedov-anar.github.io/dr.derekk/) | [index.html](index.html) | Входная страница сайта и основные сведения о враче. |
| О враче | [`/about/`](https://mamedov-anar.github.io/dr.derekk/about/) | [about/index.html](about/index.html) | Информация о враче. |
| Контакты и запись | [`/contact/`](https://mamedov-anar.github.io/dr.derekk/contact/) | [contact/index.html](contact/index.html) | Контактная информация и запись. |
| Действующий каталог процедур | [`/treatments/`](https://mamedov-anar.github.io/dr.derekk/treatments/) | [treatments/index.html](treatments/index.html) | Основной каталог с 14 существующими карточками процедур. |

## 2. Отдельные процедуры — действующие, нетестовые

Это внутренние страницы текущего каталога `/treatments/`, а не 14 дополнительных разделов верхнего уровня. При разработке нового каталога они продолжают существовать по своим адресам.

| Процедура | Адрес на сайте | Файл в репозитории |
| --- | --- | --- |
| Лазерное лечение акне | [`/treatments/acne-laser-treatment/`](https://mamedov-anar.github.io/dr.derekk/treatments/acne-laser-treatment/) | [treatments/acne-laser-treatment/index.html](treatments/acne-laser-treatment/index.html) |
| Удаление пигментации | [`/treatments/pigmentation-removal/`](https://mamedov-anar.github.io/dr.derekk/treatments/pigmentation-removal/) | [treatments/pigmentation-removal/index.html](treatments/pigmentation-removal/index.html) |
| Лазерное омоложение кожи | [`/treatments/laser-skin-rejuvenation/`](https://mamedov-anar.github.io/dr.derekk/treatments/laser-skin-rejuvenation/) | [treatments/laser-skin-rejuvenation/index.html](treatments/laser-skin-rejuvenation/index.html) |
| Hydrafacial | [`/treatments/hydrafacial/`](https://mamedov-anar.github.io/dr.derekk/treatments/hydrafacial/) | [treatments/hydrafacial/index.html](treatments/hydrafacial/index.html) |
| Химический пилинг | [`/treatments/chemical-peel/`](https://mamedov-anar.github.io/dr.derekk/treatments/chemical-peel/) | [treatments/chemical-peel/index.html](treatments/chemical-peel/index.html) |
| Микронидлинг | [`/treatments/microneedling/`](https://mamedov-anar.github.io/dr.derekk/treatments/microneedling/) | [treatments/microneedling/index.html](treatments/microneedling/index.html) |
| Коррекция овала лица | [`/treatments/jawline-filler/`](https://mamedov-anar.github.io/dr.derekk/treatments/jawline-filler/) | [treatments/jawline-filler/index.html](treatments/jawline-filler/index.html) |
| Коррекция подбородка | [`/treatments/chin-filler/`](https://mamedov-anar.github.io/dr.derekk/treatments/chin-filler/) | [treatments/chin-filler/index.html](treatments/chin-filler/index.html) |
| Коррекция скул | [`/treatments/cheek-filler/`](https://mamedov-anar.github.io/dr.derekk/treatments/cheek-filler/) | [treatments/cheek-filler/index.html](treatments/cheek-filler/index.html) |
| Коррекция губ | [`/treatments/lip-filler/`](https://mamedov-anar.github.io/dr.derekk/treatments/lip-filler/) | [treatments/lip-filler/index.html](treatments/lip-filler/index.html) |
| Коррекция морщин лба | [`/treatments/forehead-line-treatment/`](https://mamedov-anar.github.io/dr.derekk/treatments/forehead-line-treatment/) | [treatments/forehead-line-treatment/index.html](treatments/forehead-line-treatment/index.html) |
| Коррекция межбровных морщин | [`/treatments/frown-line-treatment/`](https://mamedov-anar.github.io/dr.derekk/treatments/frown-line-treatment/) | [treatments/frown-line-treatment/index.html](treatments/frown-line-treatment/index.html) |
| Коррекция «гусиных лапок» | [`/treatments/crow-s-feet-treatment/`](https://mamedov-anar.github.io/dr.derekk/treatments/crow-s-feet-treatment/) | [treatments/crow-s-feet-treatment/index.html](treatments/crow-s-feet-treatment/index.html) |
| Подтяжка бровей | [`/treatments/brow-lift/`](https://mamedov-anar.github.io/dr.derekk/treatments/brow-lift/) | [treatments/brow-lift/index.html](treatments/brow-lift/index.html) |

## 3. Правовая и служебные страницы — нетестовые

| Страница / файл | Адрес на сайте | Файл в репозитории | Роль |
| --- | --- | --- | --- |
| Политика конфиденциальности | [`/legal/privacy-policy/`](https://mamedov-anar.github.io/dr.derekk/legal/privacy-policy/) | [legal/privacy-policy/index.html](legal/privacy-policy/index.html) | Вспомогательная правовая страница |
| Страница ошибки 404 | [`/404/`](https://mamedov-anar.github.io/dr.derekk/404/) | [404/index.html](404/index.html) | Служебная страница для отсутствующих адресов |
| Обработчик 404 GitHub Pages | Срабатывает при обращении к неизвестному адресу | [404.html](404.html) | Технический файл; переводит посетителя на `/404/` |

## 4. Тестовые страницы

| Страница | Адрес на сайте | Файл в репозитории | Статус и назначение |
| --- | --- | --- | --- |
| Точная копия действующего каталога процедур | [`/treatments_2/`](https://mamedov-anar.github.io/dr.derekk/treatments_2/) | [treatments_2/index.html](treatments_2/index.html) | Тестовая копия, опубликована 2 ноября 2026 года по прямому запросу пользователя; исходная страница и основной каталог сохраняют свою роль |
| Новая страница услуг и процедур | [`/services-preview/`](https://mamedov-anar.github.io/dr.derekk/services-preview/) | [services-preview/index.html](services-preview/index.html) | Тестовая, опубликована 2 ноября 2026 года для обсуждения новой структуры из итогового Word-документа |

Особенности `/treatments_2/`:

- Полная побайтовая копия [`treatments/index.html`](treatments/index.html) из ветки `main` на коммите [`a67a8d9`](https://github.com/mamedov-anar/dr.derekk/commit/a67a8d9abeb9ad1c0e1f67552464e849fb6a21dd).
- Тексты, оформление, метаданные, встроенный код, ссылки и подключения общих ресурсов скопированы без изменений. Дополнительная отметка о тестовой версии в HTML не добавлена.
- Отдельные страницы процедур не дублировались: их исходные адреса сохранены в скопированном HTML.
- Копия доступна по прямому адресу и не добавлена в основную навигацию или исходный список `pages.json`.
- Основным действующим каталогом остаётся `/treatments/`. Отдельная тестовая версия новой структуры услуг по-прежнему находится на `/services-preview/`.

Особенности `/services-preview/`:

- Содержит 10 основных групп и 26 позиций, а также отдельные блоки ухода и подбора по запросу.
- Группы и раскрывающиеся позиции находятся внутри одной страницы. Отдельные страницы для добавленных процедур на этом этапе не создавались.
- Имеет явную тестовую отметку и ссылку на действующий каталог `/treatments/`.
- Не добавлена в основную навигацию и исходный список маршрутов `pages.json`.
- Содержит метатег `robots: noindex,nofollow`. Страница доступна по прямой ссылке; метатег задаёт указания поисковым роботам и не ограничивает доступ.
- Стили и поведение находятся в [`services-preview/services-preview.css`](services-preview/services-preview.css) и [`services-preview/services-preview.js`](services-preview/services-preview.js).
- Создана коммитом [`3bc4cae`](https://github.com/mamedov-anar/dr.derekk/commit/3bc4cae5606b80b4aced295b6bd22780075a8976). Действующая страница `/treatments/` при этом не менялась.

Перенос тестовой страницы на основной адрес или её включение в основную навигацию требует отдельного решения пользователя. До этого её статус в справочнике — **тестовая**.

## 5. Архив: страницы, которые создавались и были удалены

| Страница | Бывший путь | Текущее состояние | История |
| --- | --- | --- | --- |
| Галерея вариантов логотипа | `assets/brand/logo-exploration-2026-10-26/index.html` | Вспомогательная экспериментальная страница удалена из текущей версии 26 октября 2026 года; не входит в число действующих страниц | [Добавление: `9861c29`](https://github.com/mamedov-anar/dr.derekk/commit/9861c299189d22f4998161ce2d84083551f656d1); [удаление: `2cf8a29`](https://github.com/mamedov-anar/dr.derekk/commit/2cf8a295a58496a9e55c21dcdedfbcde723c7ad3); [исторический HTML-файл](https://github.com/mamedov-anar/dr.derekk/blob/9861c299189d22f4998161ce2d84083551f656d1/assets/brand/logo-exploration-2026-10-26/index.html) |

Оставшиеся изображения, архивы и описания в `assets/brand/logo-exploration-2026-10-26/` — материалы проекта, а не действующая страница галереи.

## 6. Источники и границы справочника

- Перечень текущих страниц сверяется с HTML-файлами ветки `main`. Удалённые страницы выявлены по истории этой ветки.
- [`pages.json`](pages.json) содержит 20 исходных маршрутов, включая `/404/`; тестовые `/services-preview/` и `/treatments_2/` учитываются отдельно в этом справочнике.
- Исходные 20 маршрутов и технический `404.html` впервые появились в репозитории при [публикации сайта `23be096`](https://github.com/mamedov-anar/dr.derekk/commit/23be096b41235a46244cfc9baa9448ac18bbabbf). Это дата появления в данном репозитории, а не дата первоначальной разработки сайта.
- Word-документы, макеты, изображения, ZIP-архивы и исторические локальные экспорты не считаются опубликованными веб-страницами.
- `README.md`, `AGENTS.md`, `PAGES.md`, `pages.json` и файлы контрольных сумм — документация и служебные данные репозитория.

## 7. Как поддерживать справочник

При создании, удалении, переименовании страницы или изменении её роли:

1. Обновить соответствующую таблицу: название, адрес, исходный файл, статус и назначение.
2. Для новой тестовой страницы указать дату, цель и связь с действующей страницей.
3. Удалённую страницу перенести в архив с коммитом удаления.
4. Пересчитать категории, количество маршрутов и HTML-файлов; обновить дату проверки.
5. Если меняется назначение каталога или навигация, согласовать это отдельно и затем зафиксировать новый статус.
6. Обновить `asset-manifest.json` и `SHA256SUMS.txt` вместе с документацией.

Наличие страницы в этом справочнике само по себе не меняет её роль, адрес или место в навигации сайта.
