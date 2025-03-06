import logging

from telethon.errors import ChannelPrivateError

from utils import logger


async def fetch_messages(client, channel_username, limit=10):
    """
    Получает последние сообщения из канала.
    :param client: Экземпляр TelegramClient.
    :param channel_username: Username канала.
    :param limit: Количество сообщений для получения.
    """
    try:
        channel = await client.get_entity(channel_username)
        logger.info(f"Получение сообщений из канала: {channel.title}")

        messages = await client.get_messages(channel, limit=limit)
        for message in messages:
            print(f"Сообщение: {message.text}")

    except ChannelPrivateError as e:
        logger.info(f"{e}")
        print(f"Канал {channel_username} является приватным или недоступным.")
    except Exception as e:
        logging.error(e)
        print(f"Ошибка при получении сообщений: {e}")
