from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.types import Message

from database.models import Users
from parser.utils import check_stop_words
from utils import logger


async def start_monitoring(client: Optional[TelegramClient], user: Users):
    @client.on(events.NewMessage(chats=user.list_channels()))
    async def handler(event):
        message = event.message
        await forward_message(message, target_channel=user.target_channel, client=client)

async def forward_message(message: Message, target_channel, client: Optional[TelegramClient]):
    try:
        if check_stop_words:
            if message.media:
                await client.send_file(entity=target_channel, file=message.media, caption=message.message)
            else:
                await client.send_message(entity=target_channel, message=message.message)
        else:
            logger.info("Обнаружено стоп слово")

    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
