# egiti
egiti (Easy GIT Ignore) - это утилита для быстрого управления gitignore-файлами в проекте

## Возможности
- Создание и удаление новых записей: `egiti add/rm .venv`
- Скачивание готовых макетов .gitignore: `egiti load C Cmake`
- Просмотр записей в файле: `egiti show --all`

## Установка
1. Через pip/pipx (проще всего)
    ```bash
    pipx install git+https://github.com/wandderq/egiti@main
    ```

2. Из исходного кода
    ```bash
    git clone https://github.com/wandderq/egiti@main
    cd egiti
    pip install .
    ```


## Лицензия
Эта утилита распространяется под [MIT лицензией](https://github.com/wandderq/egiti/blob/main/LICENSE)