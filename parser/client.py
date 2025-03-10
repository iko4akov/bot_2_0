import logging

from typing import Optional
from telethon import TelegramClient

from parser.config import api_id, api_hash
from utils import logger


class TelegramClientManager:
    def __init__(self) -> None:
        self.client = TelegramClient("session", api_id, api_hash)

    async def start(self):
        if not self.client.is_connected():
            try:
                logger.info("Запускаем клиент....")
                await self.client.start()
            except Exception as e:
                logger.error(f"Произошла ошибка: {e}")

    async def stop(self) -> None:
        if self.client.is_connected():
            await self.client.disconnect()
            logging.info("Клиент остановлен")

    async def get_client(self) -> Optional[TelegramClient]:
        return self.client
