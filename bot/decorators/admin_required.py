from typing import Callable, Awaitable

from aiogram.types import Message
from settings import config


def is_admin(user_id: int) -> bool:
    return user_id in config.ADMINS


def admin_required(handler: Callable[[Message], Awaitable[None]]) -> Callable[[Message], Awaitable[None]]:
    async def wrapper(message: Message):
        if not is_admin(message.from_user.id):
            await message.reply("У вас нет прав администратора.")
        else:
            await handler(message)
    return wrapper
