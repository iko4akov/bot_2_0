import asyncio
from threading import Thread

from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from telethon import TelegramClient

from bot.keyboard import kb
from bot.services.authorized import AuthState
from bot.services.utils import validate_phone_number
from database.models import Channel, Users
from database.services.crud_channel import add_channel, delete_channel
from database.services.crud_user import get_user, update_user
from bot import redis_cli
from utils import logger

message_router = Router()


@message_router.message(lambda m: m.text.startswith("@"))
async def create_channel(message: types.Message) -> None:
    """
    Добавляет канал в список для парсинга
    """
    channel = Channel()
    name = message.text[1:]
    channel.name = name
    channel.user_id = message.from_user.id
    await add_channel(channel)
    await message.reply(f"Канал {message.text} добавлен в ваш список", reply_markup=kb.inline_markup)

@message_router.message(lambda m: m.text.startswith("-"))
async def drop_channel(message: types.Message) -> None:
    """
    Удалить канал из списка для парсинга
    """
    name_chnanel = message.text[1:]
    await delete_channel(name_chnanel, message.from_user.id)
    await message.reply(f"Канал '{name_chnanel}' удален из списка для парсинга ", reply_markup=kb.inline_markup)


@message_router.message(StateFilter(AuthState.waiting_for_api_id))
async def process_api_id(message: types.Message, state: FSMContext) -> None:
    """Изменяет(добавляет) api_id"""

    api_id = int(message.text)
    user: Users = await get_user(message.from_user.id)
    user.api_id = api_id
    await update_user(user)
    await state.update_data(api_id=api_id)
    await message.answer("Введите API_HASh")
    await state.set_state(AuthState.waiting_for_api_hash)

@message_router.message(StateFilter(AuthState.waiting_for_api_hash))
async def process_api_hash(message: types.Message, state: FSMContext) -> None:
    """Изменяет(добавляет) api_hash"""

    api_hash = message.text
    user: Users = await get_user(message.from_user.id)
    user.api_hash = api_hash
    await update_user(user)
    await state.update_data(api_hash=api_hash)
    await message.answer("Введите телефон в формате +71234567890")
    await state.set_state(AuthState.waiting_for_phone)

@message_router.message(StateFilter(AuthState.waiting_for_phone))
async def process_phone(message: types.Message, state: FSMContext):
    """Добавляет(изменяет) номер телефона"""
    phone = message.text
    if not validate_phone_number(phone):
        await message.answer("Не правильный номер")
    user: Users = await get_user(message.from_user.id)
    user.phone = phone
    await update_user(user)
    await state.update_data(phone=phone)

    redis_cli.save_user_data(str(user.id), user.to_dict())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = TelegramClient(f"session_{user.id}", user.api_id, user.api_hash, loop=loop)

    try:
        await client.connect()
        await client.send_code_request(user.phone)
        await message.answer("Введите код подтверждения")
        await state.set_state(AuthState.waiting_for_code)

    except Exception as e:
        logger.error(f"Ошибка при отправке кода {e}")
        await message.answer(f"Ошибка при отправке кода {e}")

@message_router.message(StateFilter(AuthState.waiting_for_code))
async def process_code(message: types.Message, state: FSMContext):
    """Авторизация по коду"""
    code = message.text
    user_id = str(message.from_user.id)
    data = redis_cli.get_user_data(user_id)
    if not data:
        await message.answer("Ошибка: Данные пользователя не найдены.")
        await state.finish()
        return

    api_id = data["api_id"]
    api_hash = data["api_hash"]
    phone = data["phone"]

    client = TelegramClient(f"session_{user_id}", api_id, api_hash)

    try:
        await client.sign_in(phone, code)
        await message.answer("Авторизация прошла успешно!")
        await state.finish()

        redis_cli.save_session(user_id, {"session": "active"})

        # Thread(target=start_monitoring, args=(client, user_id)).start()

    except Exception as e:
        logger.error(f"Ошибка при авторизации: {e}")




