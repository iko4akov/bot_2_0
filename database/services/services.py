from typing import Optional

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base
from utils import logger
from database.config import CREATE_DB_COMMAND, POSTGRES_USER, CREATE_USER_COMMAND, POSTGRES_DB, POSTGRES_PASS, \
    CHECK_DB_COMMAND, CHECK_USER_COMMAND, ERROR_MESSAGE_USER, EXISTS_MESSAGE_USER, SUCCESS_MESSAGE_USER, \
    EXISTS_MESSAGE_DB, ERROR_MESSAGE_DB, SUCCESS_MESSAGE_DB


async def initialize_database(admin_engine, engine):
    """
    1. Создает нового пользователя.
    2. Создает базу данных.
    3. Создает таблицы.
    """
    async with admin_engine.connect() as conn:
        logger.info("Подключено к PostgreSQL как администратор.")
        await execute_with_check(
            conn=conn,
            check_command=CHECK_USER_COMMAND,
            create_command=CREATE_USER_COMMAND.format(username=POSTGRES_USER, password=POSTGRES_PASS),
            params={"username": POSTGRES_USER, "password": POSTGRES_PASS},
            success_message=SUCCESS_MESSAGE_USER,
            exists_message=EXISTS_MESSAGE_USER,
            error_message=ERROR_MESSAGE_USER
        )
        await execute_with_check(
            conn=conn,
            check_command=CHECK_DB_COMMAND,
            create_command=CREATE_DB_COMMAND.format(dbname=POSTGRES_DB, username=POSTGRES_USER),
            params={"dbname": POSTGRES_DB, "username": POSTGRES_USER},
            success_message=SUCCESS_MESSAGE_DB,
            exists_message=EXISTS_MESSAGE_DB,
            error_message=ERROR_MESSAGE_DB
        )

        await admin_engine.dispose()

    await create_table(engine)

async def execute_with_check(
        conn: Optional[AsyncSession],
        check_command: str,
        create_command: str,
        params: dict,
        success_message: str,
        exists_message: str,
        error_message: str
):
    """
    Универсальная функция для выполнения проверки существования объекта
    и его создания при необходимости.

    :param conn: Подключение к базе данных.
    :param check_command: SQL-команда для проверки существования объекта.
    :param create_command: SQL-команда для создания объекта.
    :param params: Параметры для SQL-команд.
    :param success_message: Сообщение о успешном создании объекта.
    :param exists_message: Сообщение о том, что объект уже существует.
    :param error_message: Сообщение об ошибке при выполнении операции.
    """
    try:
        exists = await conn.scalar(text(check_command), params)
        if not exists:
            await conn.execute(text(create_command), params)
            logger.info(success_message)
        else:
            logger.info(exists_message)
    except Exception as e:
        logger.error(f"{error_message}: {e}")

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
