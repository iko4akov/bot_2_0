from typing import Callable, Awaitable

from aiogram.types import Message

from settings.config import ADMINS

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


def admin_required(handler: Callable[[Message], Awaitable[None]]) -> Callable[[Message], Awaitable[None]]:
    async def wrapper(message: Message):
        if is_admin(message.from_user.id):
            await message.reply("У вас нет прав администратора.")
            return
        await handler(message)
    return wrapper
