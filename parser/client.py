import logging

from typing import Optional
from telethon import TelegramClient

from settings.config import API_ID, API_HASH


class TelegramClientManager:
    def __init__(self) -> None:
        self.client = TelegramClient("seeeion", API_ID, API_HASH)

    async def start(self):
        if not self.client.is_connected():
            await self.client.start()
            logging.info("Клиент запущен")

    async def stop(self) -> None:
        if self.client.is_connected():
            await self.client.disconnect()
            logging.info("Клиент остановлен")

    async def get_client(self) -> Optional[TelegramClient]:
        return self.client
