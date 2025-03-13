from telethon import TelegramClient

from bot import bot
from utils import logger


async def check_auth(api_id, api_hash, user_id, client) -> bool:


    try:
        await client.connect()
        if not await client.is_user_authorized():
            logger.warning("Пользователь не авторизован!")
            return False
        return True
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")


async def phone_provider(user_id) -> str:
    await bot.send_message(user_id, "Введите свой номер")
