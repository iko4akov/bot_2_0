#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from bot import dp, bot
from bot.handlers.handlers_admin import admin_router
from bot.handlers.handlers_callback_query import parser_router
from bot.handlers.handlers_message import message_router
from bot.handlers.handlers_start import router
from utils import logger


async def start_bot() -> None:
    """Запуск бота."""
    logger.info("Bot is starting...")

    dp.include_router(router)
    dp.include_router(parser_router)
    dp.include_router(message_router)
    dp.include_router(admin_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
