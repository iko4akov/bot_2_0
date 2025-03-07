from aiogram import Router, types

from bot import bot
from bot.keyboard import kb, DBKeyboard

from database.services.crud_channel import get_channels
from database.services.crud_user import get_user

db_router = Router()


@db_router.callback_query(lambda c: c.data == 'db')
async def show_channels(callback_query: types.CallbackQuery):
    """Показывает кнопки со всеми постами"""
    await callback_query.answer()
    user = await get_user(callback_query.from_user.id)
    channels = await get_channels(callback_query.from_user.id)
    kb_db = DBKeyboard(channels, user)
    inline_keyboard = kb_db.get_keyboard()
    if channels:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=inline_keyboard
        )
    else:
        await bot.send_message(callback_query.from_user.id, "Нет каналов", reply_markup=kb.inline_markup)
