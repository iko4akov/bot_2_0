from sqlalchemy.exc import ProgrammingError

from database import engine
from database.models import Base
from utils import logger


async def create_table():
    """Создание таблиц в бд"""
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except ProgrammingError as e:
            if "already exists" in str(e):
                logger.info("Таблицы уже существуют, игнорируем ошибку.")
            else:
                raise e
