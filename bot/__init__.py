from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import bot_token
from utils import logger


try:
    bot = Bot(
        bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()


except Exception as e:
    logger.error(f"{e}")
