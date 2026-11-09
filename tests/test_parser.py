
from primitive_db.parser import convert_value, parse_condition


def test_parse_condition():
    """Проверяет разбор условия поиска."""
    result = parse_condition("age=23")
    assert result == ("age", "23")


def test_convert_value_int():
    """Проверяет преобразование строки в число."""
    result = convert_value("23", "int")
    assert result == 23



def test_convert_value_bool():
    """Проверяет преобразование строки в логическое значение."""
    assert convert_value("true", "bool") is True
    assert convert_value("false", "bool") is False
