import math
from contextlib import suppress
from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Text
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.models import Category
from tgbot.keyboards.inline import button_back
from tgbot.keyboards.product_inline import catalog_menu_button, CategoriesCBF, CategoriesPaginateCBF, \
    ProductsPaginateCBF, products_str_button
from tgbot.models.products import Product
from tgbot.utils.pagination import Paginator

router = Router()


@router.callback_query(Text('vitrina') or CategoriesPaginateCBF.filter())
async def catalog_menu(
        callback: CallbackQuery,
        session: AsyncSession,
):
    categories = await Category.get_slice(session=session, offset=0, limit=8)
    count = await Category.get_count(session)
    keyboard = catalog_menu_button(categories=categories, page=math.ceil(count))
    await callback.message.edit_text(
        text='Это каталог. Щелкнуть на категорию, чтобы перейти на нужный продукт',
        reply_markup=keyboard
    )


@router.callback_query(CategoriesPaginateCBF.filter())
async def catalog_menu(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: CategoriesPaginateCBF,
):
    model = Paginator(model=Category)
    models, callback_data, page = await model.get_list_models(session=session,
                                                              callback_data=callback_data)
    keyboard = catalog_menu_button(models, callback_data, page)
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text='Это каталог. Щелкнуть на категорию, чтобы перейти на нужный продукт',
            reply_markup=keyboard
        )


@router.callback_query(CategoriesCBF.filter())
async def catalog_menu(
        callback: CallbackQuery,
        callback_data: CategoriesCBF,
        session: AsyncSession,
):
    category = callback_data.name

    await callback.message.edit_text(
        text=f'Категория: {category}, тест',
        reply_markup=InlineKeyboardBuilder().row(button_back).as_markup()
    )


@router.callback_query(Text('list'))
async def products_list(
        callback: CallbackQuery,
        session: AsyncSession,
):
    products, count = await Product.get_str_product(session=session,)
    await callback.message.edit_text(
        text=f'{products}',
        reply_markup=products_str_button(count)
    )


@router.callback_query(ProductsPaginateCBF.filter())
async def products_list(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: ProductsPaginateCBF
):
    products, count = await Product.get_str_product(
        session=session,
        callback_data=callback_data if callback_data else None,
    )
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text=f'{products}',
            reply_markup=products_str_button(callback_data=callback_data, count=count)
        )


@router.callback_query(Text('num'))
async def products_list(
        callback: CallbackQuery,

):
    await callback.answer()
