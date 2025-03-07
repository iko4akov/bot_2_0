from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from settings import conf


class AdminKeyboard:
    def __init__(self):
        self.inline_markup = InlineKeyboardMarkup(inline_keyboard=self.__inline_button())

    def __inline_button(self):
        self.keyboard_inline = [
            [
                InlineKeyboardButton(text=f"Спарсить из канала {conf.source_default}", callback_data="parsing"),
            ],
            [
                InlineKeyboardButton(text=f"Источник", callback_data="source"),
                InlineKeyboardButton(text=f"Цель", callback_data="target"),
            ],
            [
                InlineKeyboardButton(text=f"User", callback_data="user"),
            ],
        ]
        return self.keyboard_inline
