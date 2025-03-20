from typing import Optional

from telethon import TelegramClient
from telethon.errors import rpc_errors_re

from utils import logger


async def get_client(api_id: int, api_hash: str, user_id: int) -> Optional[TelegramClient]:
    """
    Создает и возвращает клиент Telegram.

    Args:
        api_id (int): ID API Telegram.
        api_hash (str): Хэш API Telegram.
        user_id (int): ID пользователя для создания сессии.

    Returns:
        Optional[TelegramClient]: Авторизованный клиент Telegram или None, если авторизация не удалась.
    """
    client = TelegramClient(f"session_{user_id}", api_id, api_hash)

    try:
        await client.connect()

        if not await client.is_user_authorized():
            logger.warning(f"Клиент для пользователя {user_id} не авторизован.")
            await client.disconnect()
            return None

        return client

    except rpc_errors_re as e:
        logger.error(f"Ошибка при подключении клиента для пользователя {user_id}: {e}")
        await client.disconnect()
        return None
