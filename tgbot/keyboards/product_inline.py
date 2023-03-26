from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from tgbot.models.products import Category
from tgbot.keyboards.inline import button_back


class CategoriesCBF(CallbackData, prefix="categories"):
    action: str
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
                callback_data=CategoriesCBF(action='category', name=category.name).pack()
            )
        ) for category in categories
    ]
    kb_builder.row(*buttons, width=2)
    kb_builder.row(button_back)
    return kb_builder.as_markup()
