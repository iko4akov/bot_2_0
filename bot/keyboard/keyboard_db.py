from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Users, Channel


class DBKeyboard:
    def __init__(self, channels: List[Channel], user: Users):
        self.channels = channels
        self.on_pages = 9
        self.total_pages = len(self.channels) // self.on_pages + (1 if len(self.channels) % self.on_pages != 0 else 0)
        self.len = len(self.channels)

    def _get_navigator(self) -> List[InlineKeyboardButton]:
        row = []
        if self.current_page > 0:
            row.append(
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_page")
            )
        if self.current_page < self.total_pages - 1:
            row.append(
                InlineKeyboardButton(text="➡️ Дальше", callback_data="next_page")
            )
        return row

    def get_keyboard(self):
        inline_buttons = []
        row = []
        start_index = self.current_page * self.on_pages
        end_index = start_index + self.on_pages

        for i in range(start_index, end_index):
            try:
                button = InlineKeyboardButton(
                    text=f"{self.posts[i].text[:10]}",
                    callback_data=f"|{self.posts[i].post_id}"
                )
                row.append(button)
            except IndexError:
                break

            if len(row) == 3:
                inline_buttons.append(row)
                row = []

        if row:
            inline_buttons.append(row)

        nav_button = self._get_navigator()
        if nav_button:
            inline_buttons.append(nav_button)

        return InlineKeyboardMarkup(inline_keyboard=inline_buttons)
