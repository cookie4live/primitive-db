def parse_condition(condition):
    """Разбирает условие вида column=value."""
    if "=" not in condition:
        raise ValueError("Условие должно содержать знак =.")

    column, value = condition.split("=", 1)

    column = column.strip()
    value = value.strip().strip("'\"")

    if not column or not value:
        raise ValueError("Не указано имя столбца или значение.")

    return column, value


def convert_value(value, data_type):
    """Преобразует значение в нужный тип данных."""
    if data_type == "int":
        return int(value)

    if data_type == "str":
        return str(value)

    if data_type == "bool":
        if str(value).lower() == "true":
            return True
        if str(value).lower() == "false":
            return False
        raise ValueError("Для bool используйте true или false.")

    raise ValueError(f"Неизвестный тип данных: {data_type}")
