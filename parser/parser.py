from typing import Optional

from aiogram import types
from aiogram.types import InputFile
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaDocument, DocumentAttributeVideo, Message

from bot import bot
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
            await client.send_message(target_channel, message.message)

        elif message.media and isinstance(message.media, MessageMediaPhoto):
            await client.send_file(entity=target_channel, file=message.media.photo.file_reference)

        elif message.media and isinstance(message.media, MessageMediaDocument):
            for attr in message.media.document.attributes:
                if isinstance(attr, DocumentAttributeVideo):
                    await client.send_file(
                        entity=target_channel,
                        file=message.media.document.file_reference
                    )
                    break

    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
