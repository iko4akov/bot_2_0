from aiogram import Router, types

from bot import bot
from database.models import Users, Channel
from bot.keyboard import kb
from database.services.crud_channel import add_channel, delete_channel
from database.services.crud_user import get_user, update_user
from parser.run import start_parser

parser_router = Router()


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

@parser_router.message(lambda m: m.text.startswith("@"))
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

@parser_router.message(lambda m: m.text.startswith("-"))
async def drop_channel(message: types.Message) -> None:
    """
    Удалить канал из списка для парсинга
    """
    name_chnanel = message.text[1:]
    await delete_channel(name_chnanel, message.from_user.id)
    await message.reply(f"Канал '{name_chnanel}' удален из списка для парсинга ", reply_markup=kb.inline_markup)


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

@parser_router.callback_query(lambda c: c.data == 'parsing')
async def run_parser(callback_query: types.CallbackQuery):
    """
    Команда запуска парсинга постов
    """
    await callback_query.answer("Запускаем сбор и репост постов...")
    user: Users = await get_user(callback_query.from_user.id)
    channels = [channel.name for channel in user.channel]
    await start_parser(user.api_id, user.api_hash, user.id, channels)

@parser_router.callback_query(lambda c: c.data == "stop")
async def stop_parser(callback_query: types.CallbackQuery):

    await callback_query.answer("Парсер остановлен")
