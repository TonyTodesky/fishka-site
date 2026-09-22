# Фишка.Ру

Новая сборка исследовательского архива [fishka.spb.ru](http://www.fishka.spb.ru): Astro, статический HTML, обновлённая навигация и читаемый каркас для корпуса 2003–2026 годов.

## Запуск

Нужен Node 22. Если системного нет, в репозитории лежит локальный runtime в `.tools/` (в git не попадает).

```sh
export PATH="$PWD/.tools/node/bin:$PATH"
npm install
npm run dev          # http://127.0.0.1:4321
npm run build && npm run preview   # http://127.0.0.1:4322
```

## Legacy-дамп Beget

Полный Sprutio-архив аккаунта кладётся в `legacy/` (и копия ассетов в `public/legacy/`) — оба каталога в `.gitignore`.

В дампе корень сайта — `s921183s.beget.tech/public_html` (это и есть fishka.spb.ru; `index.php` там — заглушка Beget, рабочая главная — `index.html`).

```sh
bash scripts/sync_legacy.sh "/path/to/.../s921183s.beget.tech/public_html"
npm run import:articles
npm run build
```

## Деплой на Beget

```sh
npm run build
```

Залить содержимое `dist/` в `public_html`. Старые ассеты и запасную копию пока не удалять. Пароли хостинга в репозиторий не кладём; пароль из чата стоит сменить.
