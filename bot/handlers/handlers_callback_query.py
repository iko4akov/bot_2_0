import asyncio
from threading import Thread

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from telethon import TelegramClient

from bot import bot, redis_cli
from bot.keyboard import kb
from bot.services.authorized import AuthState
from database.models import Users
from database.services.crud_user import get_user, update_user
from parser.parser import start_monitoring

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
async def run_parser(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Команда запуска парсинга постов
    """
    await callback_query.answer()
    user: Users = await get_user(callback_query.from_user.id)
    client = TelegramClient(f"session_{user.id}", user.api_id, user.api_hash)
    clients[f"{user.id}"] = client
    await client.connect()
    if not await client.is_user_authorized():
        if not user.api_id:
            await callback_query.answer("Запускаем сбор и репост постов...")
            await bot.send_message(callback_query.from_user.id, "Введите API_ID")
            await state.set_state(AuthState.waiting_for_api_id)
        elif not user.api_hash:
            await bot.send_message(callback_query.from_user.id, "Введите API_HASH")
            await state.set_state(AuthState.waiting_for_api_hash)
        elif not user.phone:
            await bot.send_message(callback_query.from_user.id, "Введите телефон")
            await state.set_state(AuthState.waiting_for_phone)
        else:
            sent_code = await client.send_code_request(user.phone)
            phone_code_hash = sent_code.phone_code_hash
            await state.update_data(phone_code_hash=phone_code_hash)

            data_user = user.to_dict()
            data_user["phone_code_hash"] = phone_code_hash
            redis_cli.save_user_data(str(user.id), data_user)

            await callback_query.answer("Код отправлен. Введите его в формате: x1xx2x3x4x5\n"
                                         "где 'x' это любой не числовой символ\n"
                                         "Пример ваш код 11111\n"
                                         "Ваше сообщение фыв1выу1выфы1ввфыв1вфы1")

            await state.set_state(AuthState.waiting_for_code)
    else:
        await bot.send_message(callback_query.from_user.id, "Парсер запущен!")
        user: Users = await get_user(callback_query.from_user.id)
        asyncio.create_task(start_monitoring(client, user))


@parser_router.callback_query(lambda c: c.data == "stop")
async def stop_parser(callback_query: types.CallbackQuery):
    client = clients.get(f"{callback_query.from_user.id}")
    if client:
        await client.disconnect()
        del clients[f"{callback_query.from_user.id}"]
        await bot.send_message(callback_query.from_user.id, "Парсер остановлен")

@parser_router.message(lambda m: m.text.lower().startswith("api+"))
async def add_api_id(message: types.Message) -> None:
    """
    Изменяет api_id, api_hash
    """
    user: Users = await get_user(message.from_user.id)
    if message.text[4:].isdigit():
        user.api_id = int(message.text[4:])
        await update_user(user)

    else:
        user.api_hash = message.text[4:]
        await update_user(user)
    await message.reply(f" {message.text} добавлен в ваш список", reply_markup=kb.inline_markup)
