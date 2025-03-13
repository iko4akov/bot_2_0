from aiogram import Router, types

from bot.keyboard import kb
from bot.services.utils import validate_phone_number
from database.models import Channel, Users
from database.services.crud_channel import add_channel, delete_channel
from database.services.crud_user import get_user, update_user

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


@message_router.message(lambda m: m.text.lower().startswith("api+"))
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

@message_router.message(lambda m: m.text.startswith("+7"))
async def get_phone(message: types.Message):
    if not validate_phone_number(message.text):
        await message.answer("Не правильный номер")
    user: Users = await get_user(message.from_user.id)
    user.phone = message.text
    await update_user(user)
