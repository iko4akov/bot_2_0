import asyncio
import logging

from aiogram.exceptions import TelegramRetryAfter

from bot import bot
from database.models.models import Media

def parse_post_id(callback_data: str) -> int:
    """
    Парсит ID поста из callback_data.
    """
    try:
        return int(callback_data[1:])
    except ValueError:
        raise ValueError("Неверный формат ID поста.")

async def send_media_files(target: [int, str], media_list: list):
    """
    Отправляет медиафайлы.
    """
    try:
        for media in media_list:
            if isinstance(media, Media):
                if media.type == "image":
                    await bot.send_photo(chat_id=target, photo=media.url)
                elif media.type == "video":
                    await bot.send_animation(chat_id=target, animation=media.url)
                await asyncio.sleep(3)
            else:
                await bot.send_message(media.post.user_id, "Медиа имеет неверный формат.")
    except TelegramRetryAfter as e:
            logging.warning(f"Сработал Flood control. Ждем {e.retry_after} секунд.")
            await asyncio.sleep(e.retry_after)
