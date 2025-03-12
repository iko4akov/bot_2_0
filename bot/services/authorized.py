from bot import bot


async def phone_provider(user_id) -> str:
    await bot.send_message(user_id, "Введите свой номер")