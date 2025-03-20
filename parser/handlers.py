from sqlite3 import OperationalError
from telethon import events, TelegramClient
from parser.monitoring import forward_message
from utils import logger


async def setup_handlers(client: TelegramClient, target_channel: str, list_channels: list[str]):
    """
    Настраивает обработчики событий для мониторинга каналов.
    """
    try:
        @client.on(events.NewMessage(chats=list_channels))
        async def handler(event):
            message = event.message
            await forward_message(message, target_channel=target_channel, client=client)
    except OperationalError as e:
        logger.error(f"Ошибка базы данных при настройке обработчиков: {e}")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при настройке обработчиков: {e}")
