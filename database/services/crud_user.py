from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database import get_session
from database.models import Users
from utils import logger


async def create_user(new_user: Users) -> bool:
    """
    Cоздает нового пользователя.
    Возвращает True, если пользователь успешно создан, и False в случае ошибки.
    """
    async for session in get_session():
        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return True
        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных при создании пользователя: {e}")
            await session.rollback()
            return False
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при создании пользователя: {e}")
            await session.rollback()
            return False

async def get_user(user_id: int) -> Optional[Users]:
    """
    Получает пользователя по tg_id.
    Возвращает объект пользователя или None, если пользователь не найден.
    """
    async for session in get_session():
        try:
            result = await session.execute(select(Users).where(Users.tg_id == user_id))
            user = result.scalars().first()
            return user
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при получении пользователя: {e}")
            return None

async def get_users() -> List[Users]:
    """
    Получает всех пользователей.
    Возвращает список пользователей.
    """
    async for session in get_session():
        try:
            result = await session.execute(select(Users))
            users = result.scalars().all()
            return users
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при получении списка пользователей: {e}")
            return []

async def update_user(updated_user: Users) -> bool:
    """
    Обновляет данные пользователя.
    Возвращает True, если пользователь был успешно обновлен, и False, если пользователь не найден.
    """
    async for session in get_session():
        try:
            result = await session.execute(select(Users).where(Users.tg_id == updated_user.tg_id))
            user = result.scalars().first()
            if not user:
                logger.warning(f"Пользователь с tg_id={updated_user.tg_id} не найден.")
                return False

            user.source = updated_user.source
            user.target = updated_user.target
            user.current_page = updated_user.current_page

            await session.commit()
            return True

        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при обновлении пользователя: {e}")
            await session.rollback()
            return False

async def delete_user(user_id: int) -> bool:
    """
    Удаляет пользователя по tg_id.
    Возвращает True, если пользователь был удален, и False, если пользователь не найден.
    """
    async for session in get_session():
        try:
            result = await session.execute(select(Users).where(Users.tg_id == user_id))
            user = result.scalars().first()
            if not user:
                logger.warning(f"Пользователь с tg_id={user_id} не найден.")
                return False

            await session.delete(user)
            await session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при удалении пользователя: {e}")
            await session.rollback()
            return False
