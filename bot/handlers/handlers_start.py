from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.models import Users
from bot.constants.constans import INFO_MESSAGE
from bot.keyboard import kb
from database.services.crud_user import create_user, get_user
from utils import logger

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Просто выкидывает меню команда: /start
    """
    logger.info(f"User started the bot: {message.from_user.id}")

    new_user = Users.from_message(message)
    check_user = await get_user(message.from_user.id)
    if not check_user:
        try:
            await create_user(new_user)
        except Exception as e:
            logger.error(f"Ошибка создания пользователя: {e}")
            await message.answer("Произошла ошибка при регистрации пользователя.")

    await message.answer(INFO_MESSAGE, reply_markup=kb.get_inline_markup())

@router.message(lambda m: m.text == 'Меню')
async def menu(message: Message):
    """
    Просто выкидывает меню команда: Меню
    """
    logger.info(f"Пользователь: {message.from_user.id} вызвал меню")
    await message.answer(INFO_MESSAGE, reply_markup=kb.get_inline_markup())
