import asyncio
import logging

from typing import Optional
from telethon import TelegramClient

from utils import logger


async def get_client(api_id, api_hash, user_id) -> Optional[TelegramClient]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(f"session{user_id}", api_id, api_hash, loop=loop)
    return client
