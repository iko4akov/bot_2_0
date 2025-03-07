from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from settings import conf


class UserKeyboard:
    def __init__(self):
        self.inline_markup = InlineKeyboardMarkup(inline_keyboard=self.__inline_button())
    def __inline_button(self):
        self.keyboard_inline = [
            [
                InlineKeyboardButton(text=f"Спарсить из канала", callback_data="parsing"),
            ],
            [
                InlineKeyboardButton(text=f"Инфа о тебе", callback_data="user"),
            ],
            [
                InlineKeyboardButton(text=f"Показать все посты", callback_data="db")
            ],
            [
                InlineKeyboardButton(text=f"Репост все", callback_data="public_all")
            ],
        ]
        return self.keyboard_inline

    def one_post(self, post_id):
        self.keyboard_one = [
            [
                InlineKeyboardButton(text="Опубликовать", callback_data=f"post{post_id}")
            ],
            [
                InlineKeyboardButton(text="Удалить", callback_data=f"delete{post_id}")
            ],
            [
                InlineKeyboardButton(text=f"Показать все посты", callback_data="db")
            ],
        ]
        return self.keyboard_one
    @staticmethod
    def markup_for_post(post_id) -> InlineKeyboardMarkup:
        inline_button = [
            [
                InlineKeyboardButton(text="Опубликовать", callback_data=f">{post_id}")
            ],
            [
                InlineKeyboardButton(text="Удалить", callback_data=f"d{post_id}")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="db")
            ],
        ]
        markup_for_post = InlineKeyboardMarkup(inline_keyboard=inline_button)
        return markup_for_post
