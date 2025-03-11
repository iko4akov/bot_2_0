from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from database.models import Base
from utils import logger
from database.config import CREATE_DB_COMMAND, POSTGRES_USER, CREATE_USER_COMMAND, POSTGRES_DB, POSTGRES_PASS, \
    CHECK_DB_COMMAND


async def initialize_database(admin_engine, engine):
    """
    1. Создает нового пользователя.
    2. Создает базу данных.
    3. Создает таблицы.
    """
    async with admin_engine.connect() as conn:
        logger.info("Подключено к PostgreSQL как администратор.")
        await create_user_db(conn)
        await create_database(conn)
        await admin_engine.dispose()

    await create_table(engine)

async def create_user_db(conn):
    """Создает нового пользователя."""
    try:
        result = await conn.execute(
            text(CREATE_USER_COMMAND.format(username=POSTGRES_USER, password=POSTGRES_PASS))
        )
        if "CREATE ROLE" in str(result):
            logger.info(f"Создан новый пользователь: {POSTGRES_USER}")
        else:
            logger.info(f"Пользователь {POSTGRES_USER} уже существует.")
    except Exception as e:
        logger.error(f"Ошибка при создании пользователя: {e}")

async def create_database(conn):
    """Создает базу данных."""
    try:
        exists = await conn.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
            {"dbname": POSTGRES_DB}
        )
        if not exists:
            await conn.execute(text(CREATE_DB_COMMAND))
            logger.info(f"База данных {POSTGRES_DB} успешно создана.")
        else:
            logger.info(f"База данных {POSTGRES_DB} уже существует.")
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {e}")

async def create_table(engine):
    """Создание таблиц в базе данных."""
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except ProgrammingError as e:
            if "already exists" in str(e):
                logger.info("Таблицы уже существуют, игнорируем ошибку.")
            else:
                logger.error(f"Ошибка при создании таблиц: {e}")
                raise
