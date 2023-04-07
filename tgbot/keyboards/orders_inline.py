import math
from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from tgbot.keyboards.inline import button_back
from tgbot.lexicon.lexicon import ORDER_BUTTON, CURRENCIES
from tgbot.keyboards.product_inline import ProductDetailCBF


def order_button(
    product_id: int
) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []

    kb_builder.row(InlineKeyboardButton(text=ORDER_BUTTON['create_order'],
                                        callback_data=ProductDetailCBF(product_id=product_id).pack()),)
    kb_builder.row(button_back)
    return kb_builder.as_markup()


def currencies_button() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    [
        buttons.append(InlineKeyboardButton(
            text=value, callback_data=key)
        ) for key, value in CURRENCIES.items()
    ]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()
