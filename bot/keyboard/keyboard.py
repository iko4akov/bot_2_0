from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


class UserKeyboard:
    """Класс для создания клавиатур пользователя."""
    @staticmethod
    def get_inline_markup() -> InlineKeyboardMarkup:
        """Создает инлайн-клавиатуру с кнопками."""
        keyboard_inline = [
            [InlineKeyboardButton(text=f"Заупстить парсинг постов", callback_data="parsing")],
            [InlineKeyboardButton(text=f"Инфа о тебе", callback_data="user")],
            [InlineKeyboardButton(text=f"Остановить парсинг постов", callback_data="stop")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard_inline)

    @staticmethod
    def get_button_markup() -> ReplyKeyboardMarkup:
        button = [[KeyboardButton(text="Меню")]]
        return ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
