# Простой парсер и конвертер

Простейший "домашний" проект для личных нужд. Предназначен для парсинга статей на сайтах (html) и конвертирования в Markdown формат для локального хранения и личного использования. 

Код не содержит комментариев - слишком маленький и самоочевидный. Комментарии излишни.

ООП не используется, в силу размера и простоты.

## `make_md.py`, `getDoc.py`

Файл `make_md.py` написан первым. Специализирован под формат статей на сайте https://webref.ru. Умеет разбирать формат таблиц на этом сайте и преобразовывать их в markdown таблицы. Файл `getDoc.py `вспомогательный и вызывает `,ake_md.py` для различных URL.

Время написания - ~3 часов.

## `parser.py`

Попытка реализовать более универсальный парсер и конвертер для статей в формате html в формат markdown. Разбор DOM производится рекурсивно. Преобразование в markdown производится на основе шаблонов тегов (набора тегов), определенных в списке `tags`. Есть возможность составлять документ из нескольких частей исходного `html`. Части определяются в списке `parts`.

Время написания - ~1 часа.
