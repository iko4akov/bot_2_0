from aiogram import Router
from aiogram.types import Message

from database.services.crud_user import get_user, get_users, delete_user
from bot.decorators.admin_required import admin_required

admin_router = Router()

@admin_router.message(lambda m: m.text.startswith("!"))
async def show_user(message: Message) -> None:
    """Показать информацию о user по айди <!id_user>"""
    id_user = int(message.text[1:])
    user = await get_user(id_user)
    await message.reply(f'Пользователь найден{user.to_dict()}')

@admin_router.message(lambda m: m.text == "/users")
@admin_required
async def get_all_users(message: Message) -> None:
    """Отобразить список всех пользователей"""
    users = await get_users()
    await message.reply(f'Пользователи найдены {users}')

@admin_router.message(lambda m: m.text.startswith("/delete"))
@admin_required
async def del_user(message: Message) -> None:
    """Удалить пользователя по id </delete<user_id>>"""
    id = int(message.text[7:])
    result = await delete_user(id)
    if result:
        await message.reply(f"Ползователь {id} deleted")
    else:
        await message.reply(f"user not finded")
