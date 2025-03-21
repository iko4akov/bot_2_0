from typing import List

from telethon.tl.types import Message
from telethon import TelegramClient

from parser.decorators import retry_on_exception
from parser.utils import remove_links, reject_message
from utils import logger


@retry_on_exception(retries=3, delay=2)
async def forward_message(message: Message, target_channel: str, client: TelegramClient):
    """
    Пересылает сообщение в целевой канал.
    """
    try:
        text = await remove_links(message.message)
        if await reject_message(text):
            if message.media:
                await client.send_file(entity=target_channel, file=message.media, caption=text)
                logger.info(f"Media отправлено в канал {target_channel} ")
            else:
                await client.send_message(entity=target_channel, message=text)
                logger.info(f"Text отправлен в канал {target_channel}")
        else:
            logger.warning(f"ОТКАЗ сообщения текст в черном списке: {text}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")


async def one_for_list(
        client: TelegramClient, target_channel: str, list_channels: List[str], num: int, limit: int = 5,
) -> None:
    """
    Пересылает несколько сообщений из указанного канала в целевой канал.

    :param client: Клиент Telegram.
    :param target_channel: Целевой канал для пересылки сообщений.
    :param list_channels: Список каналов для мониторинга.
    :param num: Номер канала в списке (начиная с 1).
    :param limit: Количество сообщений для пересылки (по умолчанию 5).
    """
    if num < 1 or num > len(list_channels):
        logger.error(f"Некорректный номер канала: {num}. Допустимый диапазон: 1-{len(list_channels)}")
        return

    source_channel = list_channels[num - 1]
    logger.info(f"Начинаем пересылку сообщений из канала: {source_channel}")

    try:
        async for message in client.iter_messages(source_channel, limit=limit):
            await forward_message(message, target_channel, client)
    except Exception as e:
        logger.error(f"Ошибка при пересылке сообщений из канала {source_channel}: {e}")
