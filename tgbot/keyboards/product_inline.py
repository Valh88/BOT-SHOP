import math
from typing import List, Optional
from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from tgbot.models.products import Category
from tgbot.keyboards.inline import button_back


class CategoriesCBF(CallbackData, prefix="categories"):
    action: str
    name: str


class ActionPage(Enum):
    NEXT = 1
    PREVIOUS = 2


class CategoriesPaginateCBF(CallbackData, prefix="slice"):
    action: str
    slice: int = 0
    current_page: int = 2


class ProductsPaginateCBF(CallbackData, prefix="products"):
    slice: int = 15
    current_page: int = 2


def products_str_button(
        count: int,
        callback_data: ProductsPaginateCBF = None,
) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    print(callback_data)
    if callback_data is None:
        button = InlineKeyboardButton(
            text='>>', callback_data=ProductsPaginateCBF().pack()
        )
        kb_builder.row(InlineKeyboardButton(text=f'1/{count}', callback_data='num'))
    else:
        button = InlineKeyboardButton(
            text='>>',
            callback_data=ProductsPaginateCBF(
                slice=callback_data.slice + 15,
                current_page=callback_data.current_page+1,
            ).pack()
        )
        kb_builder.row(
            InlineKeyboardButton(text='<<', callback_data=ProductsPaginateCBF(
                slice=callback_data.slice - 15,
                current_page=callback_data.current_page-1
            ).pack())
        )
        kb_builder.add(InlineKeyboardButton(text=f'{callback_data.current_page}/{count}', callback_data='num'))
    kb_builder.add(button)
    return kb_builder.as_markup()


def catalog_menu_button(
        categories: List[Category],
        callback_data: Optional[CategoriesPaginateCBF] = None,
        page: int = None,
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
    if callback_data:
        kb_builder.row(
            InlineKeyboardButton(
                text='<<',
                callback_data=CategoriesPaginateCBF(
                    action='previous',
                    slice=callback_data.slice - 8,
                    current_page=callback_data.current_page - 1).pack()
            )
        )
        kb_builder.add(InlineKeyboardButton(
            text=f'{callback_data.current_page}/{page}',
            callback_data=CategoriesPaginateCBF(
                action='text',
                slice=callback_data.slice,
                current_page=callback_data.current_page).pack())
        )
        kb_builder.add(
            InlineKeyboardButton(
                text='>>',
                callback_data=CategoriesPaginateCBF(
                    action='next',
                    slice=callback_data.slice + 8,
                    current_page=callback_data.current_page + 1).pack()
            )
        )
    else:
        kb_builder.row(InlineKeyboardButton(
            text='<<', callback_data=CategoriesPaginateCBF(action='previous', slice=8).pack())
        )
        kb_builder.add(InlineKeyboardButton(text=f'1/{math.ceil(page / 8)}', callback_data=0))
        kb_builder.add(InlineKeyboardButton(
            text='>>', callback_data=CategoriesPaginateCBF(action='next', slice=8).pack())
        )
    kb_builder.row(button_back)
    return kb_builder.as_markup()
