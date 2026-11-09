
from primitive_db.core import create_table


def test_create_table():
    """Проверяет создание таблицы."""
    metadata = {}

    result = create_table(
        metadata,
        "students",
        ["name:str", "age:int"],
    )

    assert "students" in result
    assert result["students"] == {
        "ID": "int",
        "name": "str",
        "age": "int",
    }



def test_create_duplicate_table():
    """Проверяет запрет на создание таблицы с одинаковым именем."""
    metadata = {
        "students": {
            "ID": "int",
            "name": "str",
        }
    }

    result = create_table(metadata, "students", ["age:int"])

    assert result == {
        "students": {
            "ID": "int",
            "name": "str",
        }
    }
