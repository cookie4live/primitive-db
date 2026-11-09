from functools import wraps
from time import monotonic


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
        start_time = monotonic()

        try:
            return func(*args, **kwargs)
        finally:
            elapsed = monotonic() - start_time
            print(
                f"Функция {func.__name__} "
                f"выполнилась за {elapsed:.3f} секунд"
            )

    return wrapper


def confirm_action(action_name):
    """Создаёт декоратор для подтверждения действия."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()

            if answer != "y":
                print("Действие отменено.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator