import asyncio
from parser.client import TelegramClientManager
from parser.channels import fetch_messages
from settings.config import CHANNELS

async def main():
    client_manager = TelegramClientManager()

    await client_manager.start()

    client = await client_manager.get_client()

    # Обрабатываем каждый канал
    for channel in CHANNELS:
        await fetch_messages(client, channel)

    # Останавливаем клиента
    await client_manager.stop()

if __name__ == '__main__':
    asyncio.run(main())

