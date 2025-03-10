from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from database import get_session
from database.models import Channel
from utils import logger


async def add_channel(new_channel: Channel) -> bool:
    """
    Cоздает channel.
    Возвращает True, если post успешно создан, и False в случае ошибки.
    """
    async for session in get_session():
        if not session:
            logger.error("Сессия не инициализирована")
            return False
        try:
            session.add(new_channel)
            await session.commit()
            await session.refresh(new_channel)
            return True
        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных при создании channel: {e}")
            await session.rollback()
            return False
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при создании channel: {e}")
            await session.rollback()
            return False


async def get_channel(channel_name: str, owner: int) -> Optional[Channel]:
    """
    Получает channel по name.
    Возвращает объект channel или None, если channel не найден.
    """
    async for session in get_session():
        try:
            result = await session.execute(select(Channel).
                                            options(joinedload(Channel.owner)).
                                            where(Channel.name == channel_name, Channel.user_id == owner)
                                            )
            channel = result.scalars().first()
            return channel
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при получении channel: {e}")
            return None


async def get_channels(owner: int) -> List[Channel]:
    """
    Получает все channels. Возвращает список channels.
    """
    async for session in get_session():
        try:
            result = await session.execute(
                select(Channel).
                options(joinedload(Channel.owner)).
                where(Channel.user_id == owner)
            )
            channels = result.unique().scalars().all()

            return channels
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при получении списка posts: {e}")
            return []

async def delete_channel(channel_name: str, owner: int) -> bool:
    """
    Удаляет channel по channel_id.
    Возвращает True, если channel был удален, и False, если channel не найден.
    """
    async for session in get_session():
        try:
            result = await session.execute(select(Channel).where(
                Channel.name == channel_name),
                Channel.user_id == owner
            )
            channel = result.scalars().first()
            if not channel:
                logger.warning(f"Channel {channel_name} не найден.")
                return False

            await session.delete(channel)
            await session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при удалении channel: {e}")
            await session.rollback()
            return False
