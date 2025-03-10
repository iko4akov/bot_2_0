#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from bot import dp, bot
from bot.handlers.handlers_admin import admin_router
from bot.handlers.handlers_user import parser_router
from bot.handlers.handlers_start import router
from utils import logger


async def start_bot() -> None:
    logger.info("Bot starting....")
    dp.include_router(router)
    dp.include_router(parser_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
