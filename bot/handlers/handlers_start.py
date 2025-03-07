from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.models.models import Users
from database.services.services import create_table
from settings import conf
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
    await message.answer(conf.error_message, reply_markup=kb.inline_markup)
