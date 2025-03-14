import logging
from typing import Optional

from telethon import TelegramClient
from telethon.errors import ChannelPrivateError

from utils import logger


async def fetch_messages(client: Optional[TelegramClient], channel_name: str, limit=10):
    """
    Получает последние сообщения из канала.
    :param client: Экземпляр TelegramClient.
    :param channel_name: Имя канала.
    :param limit: Количество сообщений для получения.
    """
    try:
        channel = await client.get_entity(channel_name)
        logger.info(f"Получение сообщений из канала: {channel.title}")

        messages = await client.get_messages(channel, limit=limit)
        for message in messages:
            print(f"Сообщение: {message.text}")

    except ChannelPrivateError as e:
        logger.info(f"{e}")
    except Exception as e:
        logging.error(f"{e}")

