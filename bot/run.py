#!/home/ko4ak/telega/bot_1.0/.venv/bin/python3
import asyncio

from aiogram.exceptions import TelegramAPIError

from bot import dp, bot
from bot.handlers import register_routers
from utils import logger


async def start_bot() -> None:
    """Запуск бота."""
    logger.info("Bot is starting...")

    register_routers(dp)

    try:
        await dp.start_polling(bot)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
