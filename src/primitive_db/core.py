from prettytable import PrettyTable

from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.parser import convert_value
from primitive_db.utils import load_table_data, save_table_data

VALID_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    """Создаёт таблицу с указанными столбцами."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}

    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        name, data_type = column.split(":", 1)

        if (
            not name
            or data_type not in VALID_TYPES
            or name in table_columns
        ):
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        table_columns[name] = data_type

    metadata[table_name] = table_columns

    columns_text = ", ".join(
        f"{name}:{data_type}"
        for name, data_type in table_columns.items()
    )

    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {columns_text}"
    )

    return metadata


@confirm_action
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


@handle_db_errors
def insert_record(metadata, table_name, values):
    """Добавляет новую запись в таблицу."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    user_columns = [name for name in columns if name != "ID"]

    if len(values) != len(user_columns):
        print("Ошибка: Количество значений не совпадает с количеством столбцов.")
        return

    records = load_table_data(table_name)

    new_id = max((record["ID"] for record in records), default=0) + 1
    new_record = {"ID": new_id}

    try:
        for column, value in zip(user_columns, values):
            data_type = columns[column]
            new_record[column] = convert_value(value, data_type)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    records.append(new_record)
    save_table_data(table_name, records)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')


@log_time
def select_records(metadata, table_name, condition=None):
    """Показывает записи таблицы с возможностью поиска."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    records = load_table_data(table_name)

    if condition is not None:
        column, value = condition

        if column not in metadata[table_name]:
            print(f"Ошибка: Столбец {column} не существует.")
            return

        try:
            value = convert_value(value, metadata[table_name][column])
        except ValueError as error:
            print(f"Ошибка: {error}")
            return

        records = [
            record for record in records
            if record[column] == value
        ]

    if not records:
        print("Записи не найдены.")
        return

    table = PrettyTable()
    table.field_names = list(metadata[table_name].keys())

    for record in records:
        table.add_row([
            record[column]
            for column in table.field_names
        ])

    print(table)


def update_record(metadata, table_name, column, new_value, condition):
    """Изменяет записи таблицы по условию."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    condition_column, condition_value = condition

    if column not in columns or condition_column not in columns:
        print("Ошибка: Указанный столбец не существует.")
        return

    if column == "ID":
        print("Ошибка: Изменять ID нельзя.")
        return

    try:
        new_value = convert_value(new_value, columns[column])
        condition_value = convert_value(
            condition_value, columns[condition_column]
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    records = load_table_data(table_name)
    updated_count = 0

    for record in records:
        if record[condition_column] == condition_value:
            record[column] = new_value
            updated_count += 1

    save_table_data(table_name, records)

    print(f"Обновлено записей: {updated_count}")


def delete_records(metadata, table_name, condition):
    """Удаляет записи из таблицы по условию."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    column, value = condition
    columns = metadata[table_name]

    if column not in columns:
        print(f'Ошибка: Столбец "{column}" не существует.')
        return

    try:
        value = convert_value(value, columns[column])
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    records = load_table_data(table_name)

    remaining_records = [
        record for record in records
        if record[column] != value
    ]

    deleted_count = len(records) - len(remaining_records)

    save_table_data(table_name, remaining_records)

    print(f"Удалено записей: {deleted_count}")


def table_info(metadata, table_name):
    """Показывает структуру таблицы."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    print(f'\nТаблица "{table_name}":')

    for column, data_type in metadata[table_name].items():
        print(f"- {column}: {data_type}")