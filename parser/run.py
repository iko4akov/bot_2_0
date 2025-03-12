#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from telethon import events
from telethon.errors import SessionPasswordNeededError

from parser.client import TelegramClientManager
from settings.config import CHANNELS

async def start_parser(api_id, api_hash, user_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = TelegramClientManager(api_id, api_hash, user_id)

    await client.start()
    print("Успешно подключились к Telegram!")

    # Проверяем, авторизованы ли мы
    if not await client.is_user_authorized():
        phone_number = input("Введите номер телефона: ")
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input('Введите код: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Введите пароль двухфакторной аутентификации: '))

    print("Авторизация успешна!")

    # Получаем объекты каналов
    channels = []
    for username in CHANNELS:
        channel = await client.get_entity(username)
        channels.append(channel)
        print(f"Подключились к каналу: {channel.title}")

    # Обработчик новых сообщений
    @client.on(events.NewMessage(chats=channels))
    async def new_message_handler(event):
        message = event.message
        channel = await event.get_chat()  # Получаем объект канала
        print(f"Новое сообщение в канале {channel.title}:")
        print(f"Отправитель: {message.sender_id}")
        print(f"Текст: {message.text}")
        print(f"Время: {message.date}")
        print("-" * 40)

    # Ожидаем новые сообщения
    print("Ожидание новых сообщений...")
    await client.run_until_disconnected()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_parser())
