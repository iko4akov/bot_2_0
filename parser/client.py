import logging

from typing import Optional
from telethon import TelegramClient

from utils import logger


client = TelegramClient(f"session{user_id}", API_ID, API_HASH)


# class TelegramClientManager:
#     def __init__(self, API_ID: int, API_HASH: str, user_id) -> None:
#         self.client = TelegramClient(f"session{user_id}", API_ID, API_HASH)
#
#     async def start(self) -> None:
#         if not self.client.is_connected():
#             try:
#                 logger.info("Запускаем клиент....")
#                 await self.client.start()
#             except Exception as e:
#                 logger.error(f"Произошла ошибка: {e}")
#
#     async def stop(self) -> None:
#         if self.client.is_connected():
#             await self.client.disconnect()
#             logging.info("Клиент остановлен")
#
#     async def get_client(self) -> Optional[TelegramClient]:
#         return self.client
#
#
