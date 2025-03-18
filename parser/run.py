import asyncio

from telethon import TelegramClient

from parser.client import get_client
from parser.handlers import setup_handlers
from parser.config import API_ID, API_HASH, target_channel, list_channels
from utils import logger


async def start_monitoring(client: TelegramClient, list_channels: list[str], target_channel: str):
    if not client:
        logger.error("Не удалось создать клиент Telegram.")
        return

    await setup_handlers(client=client, list_channels=list_channels, target_channel=target_channel)
    await client.run_until_disconnected()

if __name__ == "__main__":
    client: TelegramClient = get_client(api_id=API_ID, api_hash=API_HASH, user_id=123456)
    asyncio.run(start_monitoring(client=client, target_channel=target_channel, list_channels=list_channels))
