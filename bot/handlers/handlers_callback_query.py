from aiogram import Router, types

from bot import bot
from bot.services.authorized import check_auth
from bot.services.utils import check_data
from database.models import Users
from database.services.crud_user import get_user
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

@parser_router.callback_query(lambda c: c.data == 'parsing')
async def run_parser(callback_query: types.CallbackQuery):
    """
    Команда запуска парсинга постов
    """
    await callback_query.answer("Запускаем сбор и репост постов...")
    user: Users = await get_user(callback_query.from_user.id)
    result = await check_data(user)
    if not result["succes"]:
        bot.answer_callback_query(result["errors"])
    channels = [channel.name for channel in user.channel]
    if check_auth(user.api_id, user.api_hash, user.id):
        await start_parser(user.api_id, user.api_hash, user.id, channels)
    else:
        bot.send_message(callback_query.from_user.id, 'Введите номер телефона')


@parser_router.callback_query(lambda c: c.data == "stop")
async def stop_parser(callback_query: types.CallbackQuery):

    await callback_query.answer("Парсер остановлен")
