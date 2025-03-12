#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from parser.client import TelegramClientManager
from parser.channels import fetch_messages
from settings.config import CHANNELS

async def start_parser():
    client_manager = TelegramClientManager()

    await client_manager.start()

    client = await client_manager.get_client()

    for channel in CHANNELS:
        await fetch_messages(client, channel)

    await client_manager.stop()

if __name__ == '__main__':
    asyncio.run(start_parser())
