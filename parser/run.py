#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from telethon import events, TelegramClient

from bot.services.authorized import phone_provider
from utils import logger


async def start_parser(api_id, api_hash, user_id, channels):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = TelegramClient(f"session{user_id}", api_id, api_hash, loop=loop)

    try:
        # Подключаемся к Telegram
        await client.connect()

        # Проверяем авторизацию
        if not await client.is_user_authorized():
            logger.warning("Пользователь не авторизован!")
            phone_number = phone_provider(user_id)
            await client.send_code_request(phone_number)
            code = input("Введите код подтверждения: ")  # TODO: Заменить на получение через бота
            await client.sign_in(phone_number, code)
            logger.info("Авторизация успешна!")

        logger.info("Успешно подключились к Telegram!")

        # Обработчик новых сообщений
        @client.on(events.NewMessage(chats=channels))
        async def new_message_handler(event):
            message = event.message
            channel = await event.get_chat()  # Получаем объект канала
            logger.info(f"Новое сообщение в канале {channel.title}:")
            logger.info(f"Отправитель: {message.sender_id}")
            logger.info(f"Текст: {message.text}")
            logger.info(f"Время: {message.date}")
            logger.info("-" * 40)

        # Ожидаем новые сообщения
        logger.info("Ожидание новых сообщений...")
        await client.run_until_disconnected()

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    finally:
        # Отключаем клиента
        if client.is_connected():
            await client.disconnect()
            logger.info("Клиент остановлен.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_parser())
