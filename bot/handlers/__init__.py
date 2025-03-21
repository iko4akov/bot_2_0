from aiogram import Dispatcher

from bot.handlers.handlers_admin import admin_router
from bot.handlers.handlers_callback_query import parser_router
from bot.handlers.handlers_message import message_router
from bot.handlers.handlers_start import router


def register_routers(dp: Dispatcher) -> None:
    """Регистрация всех роутеров."""
    dp.include_router(router)
    dp.include_router(parser_router)
    dp.include_router(message_router)
    dp.include_router(admin_router)
