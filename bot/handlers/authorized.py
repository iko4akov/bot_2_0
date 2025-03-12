from aiogram import Router

authorized_router = Router()

@authorized_router.message()
async def get_phone(message: types.Message) -> None:
    name_chnanel = message.text[1:]
    await delete_channel(name_chnanel, message.from_user.id)
    await message.reply(f"Канал '{name_chnanel}' удален из списка для парсинга ", reply_markup=kb.inline_markup)
