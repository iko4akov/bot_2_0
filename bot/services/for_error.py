import logging

from aiogram.types import CallbackQuery

from bot import bot


async def handle_value_error(callback_query: CallbackQuery, error_message: str):
    """
    Обрабатывает ошибки типа ValueError.
    """
    logging.warning(f"Ошибка: {error_message}")
    await bot.send_message(callback_query.from_user.id, error_message)

async def handle_general_error(callback_query: CallbackQuery, exception: Exception):
    """
    Обрабатывает общие ошибки.
    """
    error_message = f"Произошла ошибка: {str(exception)}"
    logging.error(error_message)
    await bot.send_message(callback_query.from_user.id, error_message)
