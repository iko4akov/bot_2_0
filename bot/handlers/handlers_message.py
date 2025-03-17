import asyncio

from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from telethon import TelegramClient
from telethon.errors import PhoneCodeExpiredError

from bot.keyboard import kb
from bot.services.authorized import AuthState
from bot.services.utils import validate_phone_number
from database.models import Channel, Users
from database.services.crud_channel import add_channel, delete_channel
from database.services.crud_user import get_user, update_user
from bot import redis_cli
from parser.config import info_api_hash, info_phone, info_api_id, info_code
from parser.parser import start_monitoring
from utils import logger

message_router = Router()


@message_router.message(lambda m: m.text.startswith("@"))
async def create_channel(message: types.Message) -> None:
    """
    Изменить целевой канал
    """
    target_channel = message.text
    user: Users = await get_user(message.from_user.id)
    user.target_channel = target_channel
    await update_user(user)
    await message.reply(f"В канал {message.text} посты будут перенаправляться", reply_markup=kb.inline_markup)

@message_router.message(lambda m: m.text.startswith("https://t.me/"))
async def create_channel(message: types.Message) -> None:
    """
    Добавляет канал в список для парсинга
    """
    channel = Channel()
    name = "@" + message.text[13:]
    channel.name = name
    channel.user_id = message.from_user.id
    await add_channel(channel)
    await message.reply(f"Канал {message.text} добавлен в ваш список", reply_markup=kb.inline_markup)

@message_router.message(lambda m: m.text.startswith("-"))
async def drop_channel(message: types.Message) -> None:
    """
    Удалить канал из списка для парсинга
    """
    name_channel = message.text[1:]
    await delete_channel(name_channel, message.from_user.id)
    await message.reply(f"Канал '{name_channel}' удален из списка для парсинга ", reply_markup=kb.inline_markup)


@message_router.message(StateFilter(AuthState.waiting_for_api_id))
async def process_api_id(message: types.Message, state: FSMContext) -> None:
    """Изменяет(добавляет) api_id"""

    api_id = int(message.text)
    user: Users = await get_user(message.from_user.id)
    user.api_id = api_id
    await update_user(user)
    await state.update_data(api_id=api_id)
    if not user.api_hash:
        await message.answer(info_api_hash)
        await state.set_state(AuthState.waiting_for_api_hash)
    else:
        await message.answer(info_phone)
        await state.set_state(AuthState.waiting_for_phone)

@message_router.message(StateFilter(AuthState.waiting_for_api_hash))
async def process_api_hash(message: types.Message, state: FSMContext) -> None:
    """Изменяет(добавляет) api_hash"""

    api_hash = message.text
    user: Users = await get_user(message.from_user.id)
    user.api_hash = api_hash
    await update_user(user)
    await state.update_data(api_hash=api_hash)
    await message.answer(info_phone)
    await state.set_state(AuthState.waiting_for_phone)

@message_router.message(StateFilter(AuthState.waiting_for_phone))
async def process_phone(message: types.Message, state: FSMContext):
    """Добавляет(изменяет) номер телефона"""
    phone = message.text

    if not validate_phone_number(phone):
        await message.answer("Неправильный номер. Используйте международный формат (например, +79991234567).")
        return

    user: Users = await get_user(message.from_user.id)
    user.phone = phone
    await update_user(user)
    await state.update_data(phone=phone)

    client = TelegramClient(f"session_{user.id}", user.api_id, user.api_hash)

    try:
        await client.connect()

        if not await client.is_user_authorized():
            sent_code = await client.send_code_request(phone)
            phone_code_hash = sent_code.phone_code_hash
            await state.update_data(phone_code_hash=phone_code_hash)

            data_user = user.to_dict()
            data_user["phone_code_hash"] = phone_code_hash
            redis_cli.save_user_data(str(user.id), data_user)

            await message.answer(info_code)

            await state.set_state(AuthState.waiting_for_code)

    except Exception as e:
        logger.error(f"Ошибка при отправке кода: {e}")
        await message.answer("Произошла ошибка при отправке кода. Попробуйте снова.")
    finally:
        await client.disconnect()


@message_router.message(StateFilter(AuthState.waiting_for_code))
async def process_code(message: types.Message, state: FSMContext):
    """Авторизация по коду"""
    code = "".join([char for char in message.text if char.isdigit()])
    user_id = str(message.from_user.id)
    data = redis_cli.get_user_data(user_id)

    api_id = data["api_id"]
    api_hash = data["api_hash"]
    phone = data["phone"]
    phone_code_hash = data["phone_code_hash"]

    client = TelegramClient(f"session_{user_id}", api_id, api_hash)

    try:
        await client.connect()

        try:
            await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
            await message.answer("Авторизация прошла успешно!")
            logger.info(f"Авторизация успешна для пользователя {user_id}")
            await state.clear()

            redis_cli.save_session(user_id, {"session": "active"})

            user: Users = await get_user(message.from_user.id)

            asyncio.create_task(start_monitoring(client, user))


        except PhoneCodeExpiredError:
            await message.answer("Срок действия кода истек. Запрашиваю новый код...")
            sent_code = await client.send_code_request(phone)
            phone_code_hash = sent_code.phone_code_hash
            await state.update_data(phone_code_hash=phone_code_hash)
            await message.answer(info_code)
            return

    except Exception as e:
        logger.error(f"Ошибка при авторизации: {e}")
        await message.answer("Произошла ошибка при авторизации. Попробуйте снова.")
    finally:
        await client.disconnect()
