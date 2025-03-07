import logging
from datetime import datetime

from sqlalchemy.exc import ProgrammingError

from database import engine, get_session
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


async def add_posts(posts: list, tg_id):
    """
    Добавляет посты и связанные медиафайлы в базу данных.
    Если обнаружены дубликаты медиафайлов, пост не создается.
    """
    async for session in get_session():
        try:
            duplicate_logs = []

            for post in posts:
                media_duplicates = await check_media_duplicates(session, post)

                if media_duplicates:
                    duplicate_logs += media_duplicates
                    continue

                new_post = Post(
                    user_id=tg_id,
                    text=post.get('text'),
                    created_at=datetime.now()
                )
                session.add(new_post)
                await session.flush()

                await process_media(session, new_post, post)

                await session.commit()

            if duplicate_logs:
                logging.warning("Обнаружены дубликаты медиафайлов:")
                for log in duplicate_logs:
                    logging.warning(log)

        except Exception as e:
            await session.rollback()
            logging.error(f"Ошибка при добавлении постов: {str(e)}")
            raise
