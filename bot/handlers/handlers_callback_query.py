import asyncio

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from telethon import TelegramClient

from bot import bot, redis_cli
from bot.keyboard import kb
from bot.services.authorized import AuthState
from database.models import Users
from database.services.crud_user import get_user, update_user
from parser.client import get_client
from parser.monitoring import one_for_list
from parser.run import start_monitoring
from parser.config import info_code, info_phone, info_api_id, info_api_hash
from utils import logger

parser_router = Router()

clients = {}

@parser_router.callback_query(lambda c: c.data == 'user')
async def callback_user(callback_query: types.CallbackQuery):
    """
    Обрабатывает команду user. Возвращает информацию о пользователе
    """
    await callback_query.answer()
    id = callback_query.from_user.id
    user: Users = await get_user(id)
    if user:
        await bot.answer_callback_query(callback_query.id, f'Готово')
        await bot.send_message(callback_query.from_user.id, f'{user.info()}')
    else:
        await bot.answer_callback_query(callback_query.id, f'user not finded')

@parser_router.callback_query(lambda c: c.data == 'parsing')
async def run_parser(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Команда запуска парсинга постов.
    """
    await callback_query.answer()
    user: Users = await get_user(callback_query.from_user.id)
    client = await get_client(api_id=user.api_id, api_hash=user.api_hash, user_id=user.id)
    clients[f"{user.id}"] = client

    try:
        await client.connect()
        if not await client.is_user_authorized():
            if not user.api_id:
                await callback_query.answer("Запускаем сбор и репост постов...")
                await bot.send_message(callback_query.from_user.id, info_api_id)
                await state.set_state(AuthState.waiting_for_api_id)
            elif not user.api_hash:
                await bot.send_message(callback_query.from_user.id, info_api_hash)
                await state.set_state(AuthState.waiting_for_api_hash)
            elif not user.phone:
                await bot.send_message(callback_query.from_user.id, info_phone)
                await state.set_state(AuthState.waiting_for_phone)
            else:
                sent_code = await client.send_code_request(user.phone)
                phone_code_hash = sent_code.phone_code_hash
                await state.update_data(phone_code_hash=phone_code_hash)

                data_user = user.to_dict()
                data_user["phone_code_hash"] = phone_code_hash
                redis_cli.save_user_data(str(user.id), data_user)

                await callback_query.answer(info_code)

                await state.set_state(AuthState.waiting_for_code)

        else:
            await bot.send_message(callback_query.from_user.id, "Парсер запущен!")
            asyncio.create_task(start_monitoring(client, user.list_channels(), user.target_channel))
    except ConnectionError as e:
        logger.error(f"Ошибка подключения: {e}")
        await bot.send_message(callback_query.from_user.id, "Не удалось подключиться к Telegram.")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        await bot.send_message(callback_query.from_user.id, "Произошла ошибка при запуске парсера.")

@parser_router.callback_query(lambda c: c.data == "stop")
async def stop_parser(callback_query: types.CallbackQuery) -> None:
    """
    Команда остановки парсера.
    """
    await callback_query.answer()
    user_id = str(callback_query.from_user.id)
    client = clients.get(user_id)

    if client:
        try:
            await client.disconnect()
            del clients[user_id]
            await bot.send_message(callback_query.from_user.id, "Парсер остановлен")
        except Exception as e:
            logger.error(f"Ошибка при остановке парсера: {e}")
            await bot.send_message(callback_query.from_user.id, "Произошла ошибка при остановке парсера.")
    else:
        await bot.send_message(callback_query.from_user.id, "Парсер не был запущен.")

@parser_router.message(lambda m: m.text.lower().startswith("api+"))
async def add_api_id(message: types.Message) -> None:
    """
    Изменяет api_id и api_hash пользователя.
    """
    user = await get_user(message.from_user.id)
    api_data = message.text[4:].strip()

    if api_data.isdigit():
        user.api_id = int(api_data)
        await update_user(user)
        await message.reply(f"API_ID {api_data} успешно добавлен.", reply_markup=kb.inline_markup)
    elif len(api_data) == 32:
        user.api_hash = api_data
        await update_user(user)
        await message.reply(f"API_HASH {api_data} успешно добавлен.", reply_markup=kb.inline_markup)
    else:
        await message.reply("Некорректный формат API_ID или API_HASH. Пожалуйста, попробуйте снова.")

@parser_router.message(lambda m: m.text.lower().startswith("один"))
async def one_for(message: types.Message):
    num = int(message.text[4])
    limit = int(message.text[6])
    user: Users = await get_user(message.from_user.id)
    list_channels = user.list_channels()
    target_channel = user.target_channel
    client = clients.get(message.from_user.id)

    await one_for_list(client=client, limit=limit, num=num, list_channels=list_channels, target_channel=target_channel)
