import shlex

from primitive_db.constants import META_FILE
from primitive_db.core import (
    create_table,
    delete_records,
    drop_table,
    insert_record,
    select_records,
    table_info,
    update_record,
)
from primitive_db.parser import parse_condition
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Выводит справку по командам."""
    print("\n*** Справка по командам ***")
    print("help — показать справку")
    print("exit — выйти из программы")
    print("create_table <имя> <столбец:тип> ... — создать таблицу")
    print("drop_table <имя> — удалить таблицу")
    print("list_tables — показать список таблиц")
    print("info <имя> — показать структуру таблицы")
    print("insert into <таблица> values (...) — добавить запись")
    print("select from <таблица> [where условие] — показать записи")
    print("update <таблица> set <поле>=<значение> where <условие> — изменить запись")
    print("delete from <таблица> where <условие> — удалить записи")



def run():
    """Запускает программу и обрабатывает команды."""
    print_help()

    while True:
        metadata = load_metadata(META_FILE)
        user_input = input("\nВведите команду: ").strip()

        try:
            args = shlex.split(user_input, posix=False)
        except ValueError as error:
            print(f"Ошибка ввода: {error}")
            continue

        if not args:
            continue

        command = args[0]


        if command == "help":
            print_help()

        elif command == "exit":
            print("Выход из программы.")
            break

        elif command == "create_table":
            if len(args) < 3:
                print("Ошибка: Укажите имя таблицы и столбцы.")
                continue

            table_name = args[1]
            metadata = create_table(metadata, table_name, args[2:])
            save_metadata(META_FILE, metadata)

        elif command == "insert":
            if len(args) < 5 or args[1] != "into" or args[3] != "values":
                print("Ошибка: Используйте insert into <таблица> values (...)")
                continue

            table_name = args[2]
            values_text = " ".join(args[4:]).strip()

            if not values_text.startswith("(") or not values_text.endswith(")"):
                print("Ошибка: Значения должны быть указаны в скобках.")
                continue

            values_text = values_text[1:-1]
            values = [
                value.strip().strip("'\"")
                for value in values_text.split(",")
            ]

            insert_record(metadata, table_name, values)
        elif command == "drop_table":
            if len(args) != 2:
                print("Ошибка: Укажите имя таблицы.")
                continue

            drop_table(metadata, args[1])
            save_metadata("db_meta.json", metadata)
        elif command == "select":
            if len(args) < 3 or args[1] != "from":
                print("Ошибка: Используйте select from <таблица> [where условие]")
                continue

            table_name = args[2]

            if len(args) == 3:
                select_records(metadata, table_name)

            elif len(args) >= 5 and args[3] == "where":
                try:
                    condition = parse_condition(" ".join(args[4:]))
                    select_records(metadata, table_name, condition)
                except ValueError as error:
                    print(f"Ошибка: {error}")

            else:
                print("Ошибка: Неверный формат команды select.")
        elif command == "update":
            if len(args) < 6 or args[2] != "set" or "where" not in args:
                print(
                    "Ошибка: Используйте update <таблица> "
                    "set <поле>=<значение> where <условие>"
                )
                continue

            table_name = args[1]
            where_index = args.index("where")

            try:
                assignment = " ".join(args[3:where_index])
                column, new_value = parse_condition(assignment)

                condition_text = " ".join(args[where_index + 1:])
                condition = parse_condition(condition_text)

                update_record(
                    metadata,
                    table_name,
                    column,
                    new_value,
                    condition,
                )
            except ValueError as error:
                print(f"Ошибка: {error}")
        elif command == "delete":
            if len(args) < 5 or args[1] != "from" or args[3] != "where":
                print("Ошибка: Используйте delete from <таблица> where <условие>")
                continue

            table_name = args[2]

            try:
                condition = parse_condition(" ".join(args[4:]))
                delete_records(metadata, table_name, condition)
            except ValueError as error:
                print(f"Ошибка: {error}")
        elif command == "info":
            if len(args) != 2:
                print("Ошибка: Используйте info <имя_таблицы>")
                continue

            table_info(metadata, args[1])
        elif command == "list_tables":
            if metadata:
                for table_name in metadata:
                    print(f"- {table_name}")
            else:
                print("Таблиц пока нет.")

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
