from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.models import Users
from database.services.services import create_table
from constants.constans import INFO_MESSAGE
from bot.keyboard import kb
from database.services.crud_user import create_user

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Просто выкидывает меню команда: /start
    """
    await create_table()
    new_user = Users.from_message(message)

    await create_user(new_user)
    await message.answer(INFO_MESSAGE, reply_markup=kb.inline_markup)
    await message.answer(INFO_MESSAGE, reply_markup=kb.button_markup)

@router.message(lambda m: m.text == 'Меню')
async def menu(message: Message):
    """
    Просто выкидывает меню команда: Меню
    """
    await message.answer(INFO_MESSAGE, reply_markup=kb.inline_markup)
