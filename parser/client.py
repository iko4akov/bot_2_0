import asyncio

from typing import Optional
from telethon import TelegramClient


async def get_client(api_id, api_hash, user_id) -> Optional[TelegramClient]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(f"session_{user_id}", api_id, api_hash, loop=loop)
    return client
