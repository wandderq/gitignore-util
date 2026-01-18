# gitignore-util
gitignore-util - это утилита для быстрого управления .gitignore файлами в проекте

## Возможности
- Создание и удаление новых записей: `gitignore add/rm .venv`
- Скачивание готовых макетов .gitignore: `gitignore load C Cmake`
- Просмотр записей в файле: `gitignore show --all`

## Установка
1. Через pip/pipx (проще всего)
    ```bash
    pipx install git+https://github.com/wandderq/gitignore-util@main
    ```

2. Из исходного кода
    ```bash
    git clone https://github.com/wandderq/gitignore-util@main
    cd gitignore-util
    pip install . # используйте -e для сборки в режиме разработки
    ```


## Лицензия
Эта утилита распространяется под [MIT лицензией](https://github.com/wandderq/gitignore-util/blob/main/LICENSE)