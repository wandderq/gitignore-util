# gitignore
gitignore - это простая утилита для управления .gitignore файлом вашего проекта


## Возможности
- Создание новых записей: `gitignore add .vscode .venv`
- Просмотр текущих записей: `gitignore show`
- Удаление записей: `gitignore rm .python-version`

## Установка
Утилита устанавливается как pip-пакет, так что вы можете использовать pipx
```
pip install git+https://github.com/wandderq/gitignore-util@main
```