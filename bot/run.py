#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from bot import dp, bot
from bot.handlers.handlers_admin import admin_router
from bot.handlers.handlers_callback_query import parser_router
from bot.handlers.handlers_message import message_router
from bot.handlers.handlers_start import router
from utils import logger


async def start_bot() -> None:
    logger.info("Bot running....")
    routers = [router, parser_router, message_router, admin_router]
    # dp.include_router(router)
    # dp.include_router(parser_router)
    # dp.include_router(message_router)
    # dp.include_router(admin_router)
    dp.include_routers(routers)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
