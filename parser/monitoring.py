from typing import Optional

from telethon.tl.types import Message
from telethon import TelegramClient

from parser.utils import remove_links
from utils import logger


async def forward_message(message: Message, target_channel: str, client: TelegramClient):
    """
    Пересылает сообщение в целевой канал.
    """
    try:
        text = await remove_links(message.message)
        if message.media:
            await client.send_file(entity=target_channel, file=message.media, caption=text)
            logger.info("Media отправлено")
        else:
            await client.send_message(entity=target_channel, message=text)
            logger.info("Text отправлен")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

#
# async def one_for_list(client: TelegramClient, target_channel, num: int, limit: int = 5, list_channels: Optional[str]):
#     """
#     Пересылает несколько сообщений из указанного канала.
#     """
#     source = list_channels[num - 1]
#     async for message in client.iter_messages(source, limit=limit):
#         await forward_message(message, target_channel, client)