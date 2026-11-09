
# Primitive DB

Primitive DB — простая консольная база данных на Python.

## Описание

Учебный проект, реализующий базу данных с хранением
информации в JSON-файлах.

Программа позволяет:
- Создавать и удалять таблицы.
- Просматривать список таблиц и их структуру.
- Добавлять записи.
- Искать и просматривать записи.
- Изменять и удалять записи.

## Технологии

- Python 3.12
- uv
- JSON
- PrettyTable
- Ruff
- pytest

## Установка

```bash
uv sync
```

## Запуск

```bash
uv run project
```

## Команды

Создание таблицы:

```text
create_table students name:str age:int
```

Просмотр списка таблиц:

```text
list_tables
```

Просмотр структуры таблицы:

```text
info students
```

Добавление записи:

```text
insert into students values ("Анна", 22)
```

Просмотр записей:

```text
select from students
```

Поиск по условию:

```text
select from students where age=22
```

Изменение записи:

```text
update students set age=23 where ID=1
```

Удаление записи:

```text
delete from students where ID=1
```

Удаление таблицы:

```text
drop_table students
```

Справка:

```text
help
```

Выход:

```text
exit
```

## Проверка качества кода

```bash
uv run ruff check .
```

## Запуск тестов

```bash
uv run pytest -v
```

## Сборка проекта

```bash
uv build
uvx twine check dist/*
```
