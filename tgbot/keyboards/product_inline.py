import math
from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from tgbot.keyboards.inline import button_back


class CategoriesCBF(CallbackData, prefix="categories"):
    action: str
    category_id: Optional[int] = None


class CategoriesPaginateCBF(CallbackData, prefix="slice"):
    action: str
    slice: int = 0
    current_page: int = 2


class ProductsPaginateCBF(CallbackData, prefix="products"):
    slice: int = 15
    current_page: int = 2


class ProductsCatalogPaginateCBF(CallbackData, prefix="by_catalog"):
    slice: int = 15
    current_page: int = 2
    category_id: int


class ProductDetailCBF(CallbackData, prefix="prod_detail"):
    product: str = 'product'
    product_id: int


def products_str_button(
        count: int,
        callback_data: ProductsPaginateCBF = None,
) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    if callback_data is None:
        kb_builder.row(
            InlineKeyboardButton(text='<<', callback_data=ProductsPaginateCBF().pack())
        )
        button = InlineKeyboardButton(
            text='>>', callback_data=ProductsPaginateCBF().pack()
        )
        kb_builder.add(InlineKeyboardButton(text=f'1/{count}', callback_data='num'))
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
    kb_builder.row(button_back)
    return kb_builder.as_markup()


def catalog_menu_button(
        categories: List,
        callback_data: Optional[CategoriesPaginateCBF] = None,
        page: int = None,
) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    [
        buttons.append(
            InlineKeyboardButton(
                text=category.name,
                callback_data=CategoriesCBF(action='category', category_id=category.id).pack()
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
        kb_builder.add(InlineKeyboardButton(text=f'1/{math.ceil(page / 8)}', callback_data='num'))
        kb_builder.add(InlineKeyboardButton(
            text='>>', callback_data=CategoriesPaginateCBF(action='next', slice=8).pack())
        )
    kb_builder.row(button_back)
    return kb_builder.as_markup()


def products_button(
        count: int,
        products: List['Product'],
        callback_data: Optional[ProductsCatalogPaginateCBF] = None,
) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    [
        buttons.append(InlineKeyboardButton(
            text=product.name + product.description,
            callback_data=ProductDetailCBF(product_id=product.id).pack()
            )
        ) for product in products
    ]

    kb_builder.row(*buttons, width=1)
    if callback_data is None:
        kb_builder.row(
            InlineKeyboardButton(
                text='<<',
                callback_data=ProductsCatalogPaginateCBF(
                   category_id=products[0].category_id
                ).pack())
        )
        button = InlineKeyboardButton(
            text='>>',
            callback_data=ProductsCatalogPaginateCBF(
                category_id=products[0].category_id
            ).pack()
        )
        kb_builder.add(InlineKeyboardButton(text=f'1/{math.ceil(count/8)}', callback_data='num'))
    else:
        button = InlineKeyboardButton(
            text='>>',
            callback_data=ProductsCatalogPaginateCBF(
                slice=callback_data.slice + 8,
                current_page=callback_data.current_page + 1,
                category_id=callback_data.category_id,
            ).pack()
        )
        kb_builder.row(
            InlineKeyboardButton(text='<<', callback_data=ProductsCatalogPaginateCBF(
                slice=callback_data.slice - 8,
                current_page=callback_data.current_page - 1,
                category_id=callback_data.category_id,
            ).pack())
        )
        kb_builder.add(InlineKeyboardButton(text=f'{callback_data.current_page}/{count}', callback_data='num'))
    kb_builder.add(button)
    kb_builder.row(button_back)
    return kb_builder.as_markup()
