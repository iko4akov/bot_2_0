#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from bot import dp, bot
from bot.handlers.handlers_admin import admin_router
from bot.handlers.handlers_datatbase import db_router
from bot.handlers.handlers_user import parser_router
from bot.handlers.handlers_start import router


async def main() -> None:
    dp.include_router(router)
    dp.include_router(parser_router)
    dp.include_router(admin_router)
    dp.include_router(db_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
