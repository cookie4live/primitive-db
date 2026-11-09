
import json
from pathlib import Path


def create_cacher():
    """Создаёт кеш для хранения результатов."""
    cache = {}

    def cache_result(key, value_func):
        if key not in cache:
            cache[key] = value_func()

        return cache[key]

    def clear_cache():
        cache.clear()

    cache_result.clear_cache = clear_cache
    return cache_result


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


cache_result = create_cacher()


def load_table_data(table_name):
    """Загружает записи таблицы с использованием кеша."""

    def read_data():
        filepath = Path("data") / f"{table_name}.json"

        try:
            with open(filepath, encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    return cache_result(table_name, read_data)


def save_table_data(table_name, records):
    """Сохраняет записи таблицы в JSON-файл."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    filepath = data_dir / f"{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

    cache_result.clear_cache()

