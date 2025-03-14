import base64
from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaDocument, DocumentAttributeVideo, Message

from database.models import Users
from utils import logger


async def start_monitoring(client: Optional[TelegramClient], user: Users):
    @client.on(events.NewMessage(chats=user.list_channels()))
    async def handler(event):
        message = event.message
        print(message)
        await forward_message(message, target_channel=user.id, client=client)

async def forward_message(message: Message, target_channel, client: Optional[TelegramClient]):
    try:
        if message.message:
            await client.send_message(entity=target_channel, message=message.message)

        elif message.media:
            await client.send_file(entity=target_channel, file=message.media)

    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
