#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from parser.config import api_id, api_hash
from telethon import TelegramClient


async def start_parser(user_id: str, api_id: int, api_hash: str):
    client = TelegramClient(session=f"session_{user_id}", api_id=api_id, api_hash=api_hash)
    pass



#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(start_parser())
