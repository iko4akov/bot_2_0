from aiogram import Router
from aiogram.types import Message

from database.services.crud_user import get_user, get_users, delete_user
from bot.decorators.admin_required import admin_required

admin_router = Router()


@admin_router.message(lambda m: m.text.startswith("!"))
@admin_required
async def show_user(message: Message) -> None:
    """
    Показать информацию о пользователе по ID.
    Команда: !<user_id>
    """
    try:
        user_id = int(message.text[1:])

        user = await get_user(user_id)
        if user:
            await message.reply(f"Пользователь найден:\n{user.to_dict()}")
        else:
            await message.reply("Пользователь с таким ID не найден.")
    except ValueError:
        await message.reply("Некорректный формат ID. Используйте: !<user_id>")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")


@admin_router.message(lambda m: m.text == "/users")
@admin_required
async def list_all_users(message: Message) -> None:
    """
    Отобразить список всех пользователей.
    Команда: /users
    """
    try:
        users = await get_users()
        if users:
            user_list = "\n".join([f"{user.id}: {user.username}" for user in users])
            await message.reply(f"Список пользователей:\n{user_list}")
        else:
            await message.reply("Пользователи не найдены.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")


@admin_router.message(lambda m: m.text.startswith("/delete"))
@admin_required
async def delete_user_by_id(message: Message) -> None:
    """
    Удалить пользователя по ID.
    Команда: /delete<user_id>
    """
    try:
        user_id = int(message.text[7:])

        is_deleted = await delete_user(user_id)
        if is_deleted:
            await message.reply(f"Пользователь с ID {user_id} успешно удален.")
        else:
            await message.reply(f"Пользователь с ID {user_id} не найден.")
    except ValueError:
        await message.reply("Некорректный формат ID. Используйте: /delete<user_id>")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")
