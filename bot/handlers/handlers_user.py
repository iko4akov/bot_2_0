import logging

from aiogram import Router, types

from bot import bot
from database.models import Users, Channel
from bot.keyboard import kb
from database.services.crud_channel import add_channel, delete_channel
from database.services.crud_user import get_user

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
        await bot.send_message(callback_query.from_user.id, f'{user.to_dict()}')
    else:
        await bot.answer_callback_query(callback_query.id, f'user not finded')

@parser_router.message(lambda m: m.text.startswith("@"))
async def set_target(message: types.Message) -> None:
    """
    Добавляет канал в список для парсинга
    """
    channel = Channel()
    channel.name = message.text[1:]
    channel.user_id = message.from_user.id
    await add_channel(channel)
    await message.reply(f"Канал {message.text} добавлен в ваш список", reply_markup=kb.inline_markup)

@parser_router.message(lambda m: m.text.startswith("-"))
async def set_source(message: types.Message) -> None:
    """
    Удалить канал из списка для парсинга
    """
    name_chnanel = message.text[1:]
    await delete_channel(name_chnanel, message.from_user.id)
    await message.reply(f"Канал '{name_chnanel}' удален из списка для парсинга ", reply_markup=kb.inline_markup)

@parser_router.callback_query(lambda c: c.data == 'parsing')
async def parsing(callback_query: types.CallbackQuery):
    """
    Команда парсинга из канала source
    """
    await callback_query.answer("Начинаем собирать посты.....")
    try:
        user = await get_user(callback_query.from_user.id)

        posts = parser_posts(user.source)

        await add_posts(posts, callback_query.from_user.id)

        await bot.send_message(
            callback_query.from_user.id,
            f"Собрали {len(posts)} новых постов",
            reply_markup=kb.inline_markup
        )
    except Exception as e:
        logging.error(f"Ошибка при парсинге: {str(e)}")
        await bot.send_message(
            callback_query.from_user.id,
            "Произошла ошибка при сборе постов. Пожалуйста, попробуйте позже."
        )
