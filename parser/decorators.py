import asyncio
from sqlite3 import OperationalError

from utils import logger


def retry_on_exception(retries=3, delay=1):
    """
    Декоратор для повторных попыток выполнения функции в случае ошибки.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except OperationalError as e:
                    logger.error(f"Ошибка базы данных (попытка {attempt + 1}): {e}")
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
                    else:
                        raise
                except Exception as e:
                    logger.error(f"Непредвиденная ошибка (попытка {attempt + 1}): {e}")
                    raise
        return wrapper
    return decorator
