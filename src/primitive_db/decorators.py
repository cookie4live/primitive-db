from functools import wraps
from time import perf_counter


def handle_db_errors(func):
    """Обрабатывает ошибки при выполнении функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, KeyError, OSError) as error:
            print(f"Ошибка базы данных: {error}")
            return None

    return wrapper
def log_time(func):
    """Измеряет время выполнения функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = perf_counter() - start_time
            print(f"Время выполнения: {elapsed:.4f} сек.")

    return wrapper


def confirm_action(func):
    """Запрашивает подтверждение перед выполнением действия."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        answer = input("Вы уверены? [y/n]: ").strip().lower()

        if answer != "y":
            print("Действие отменено.")
            return None

        return func(*args, **kwargs)

    return wrapper