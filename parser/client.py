from typing import Optional
from telethon import TelegramClient

from utils import logger


async def get_client(api_id: str, api_hash: str, user_id: int) -> Optional[TelegramClient]:
    """
    Создает и возвращает клиент Telegram.
    """
    client = TelegramClient(f"session_{user_id}", api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        logger.warning(f"Клиент для пользователя {user_id} не авторизован.")
        return None
    return client
