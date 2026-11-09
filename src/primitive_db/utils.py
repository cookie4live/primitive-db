
import json
from functools import wraps
from pathlib import Path


def create_cacher():
    """Создаёт декоратор для кеширования результатов."""
    cache = {}

    def cacher(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = repr((args, sorted(kwargs.items())))

            if key not in cache:
                cache[key] = func(*args, **kwargs)

            return cache[key]

        def clear_cache():
            cache.clear()

        wrapper.clear_cache = clear_cache
        return wrapper

    return cacher


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла."""
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@create_cacher()
def load_table_data(table_name):
    """Загружает записи таблицы из JSON-файла."""
    filepath = Path("data") / f"{table_name}.json"

    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, records):
    """Сохраняет записи таблицы в JSON-файл."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    filepath = data_dir / f"{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

    load_table_data.clear_cache()

