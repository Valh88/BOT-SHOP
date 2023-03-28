from typing import List
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.models.products import Category


class AdminCBF(CallbackData, prefix="admin"):
    action: str = 'admin'
    name: str


def catalog_menu_button(
        categories: List[Category],
) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    [
        buttons.append(
            InlineKeyboardButton(
                text=category.name,
                callback_data=AdminCBF(name=category.name).pack()
            )
        ) for category in categories
    ]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()
