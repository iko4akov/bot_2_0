from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


class UserKeyboard:
    def __init__(self):
        self.inline_markup = InlineKeyboardMarkup(inline_keyboard=self.__inline_button())
        self.button_markup = ReplyKeyboardMarkup(keyboard=self.__button())
    @staticmethod
    def __inline_button():
        keyboard_inline = [
            [
                InlineKeyboardButton(text=f"Заупстить парсинг постов", callback_data="parsing"),
            ],
            [
                InlineKeyboardButton(text=f"Инфа о тебе", callback_data="user"),
            ],
            [
                InlineKeyboardButton(text=f"Показать список ваших каналов", callback_data="list")
            ],
            [
                InlineKeyboardButton(text=f"Остановить парсинг постов", callback_data="stop")
            ],
        ]
        return keyboard_inline

    @staticmethod
    def __button():
        button = [
            [
                KeyboardButton(text="Меню")
            ]
        ]
        return button
