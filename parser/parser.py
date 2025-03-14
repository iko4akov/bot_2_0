import logging
from typing import Optional

from telethon import TelegramClient, events
from telethon.errors import ChannelPrivateError

from bot import bot
from database.models import Users
from utils import logger


async def start_monitoring(client: Optional[TelegramClient], user: Users):

    @client.on(events.NewMessage(chats=user.list_channels()))
    async def handler(event):
        message = event.message
        bot.send_message(user.id, message)

    # Запускаем клиент Telethon
    client.loop.run_until_complete(client.run_until_disconnected())


