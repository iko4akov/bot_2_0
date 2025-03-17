from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.types import Message

from database.models import Users
from parser.utils import remove_links
from utils import logger


async def start_monitoring(client: Optional[TelegramClient], user: Users):
    @client.on(events.NewMessage(chats=user.list_channels()))
    async def handler(event):
        message = event.message
        await forward_message(message, target_channel=user.target_channel, client=client)

async def forward_message(message: Message, target_channel, client: Optional[TelegramClient]):
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

async def one_for_list(client: Optional[TelegramClient], user: Users, num: int, limit: int = 5):
    source = user.list_channels()[num-1]
    for message in client.iter_messages(source, limit=limit):
        await forward_message(message, user.target_channel, client)
