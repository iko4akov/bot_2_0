from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot import bot
from bot.keyboard import kb
from bot.services.authorized import AuthState
from database.models import Users
from database.services.crud_user import get_user, update_user

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
async def run_parser(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Команда запуска парсинга постов
    """
    user: Users = await get_user(callback_query.from_user.id)
    if not user.api_id:
        await callback_query.answer("Запускаем сбор и репост постов...")
        await bot.send_message(callback_query.from_user.id, "Введите API_ID")
        await state.set_state(AuthState.waiting_for_api_id)
    elif not user.api_hash:
        await bot.send_message(callback_query.from_user.id, "Введите API_HASH")
        await state.set_state(AuthState.waiting_for_api_hash)
    else:
        await bot.send_message(callback_query.from_user.id, "Введите телефон")
        await state.set_state(AuthState.waiting_for_phone)



@parser_router.callback_query(lambda c: c.data == "stop")
async def stop_parser(callback_query: types.CallbackQuery):

    await callback_query.answer("Парсер остановлен")

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
