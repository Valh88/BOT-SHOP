import math
from contextlib import suppress
from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Text
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.crud import category
from tgbot.models.models import Category
from tgbot.keyboards.inline import button_back
from tgbot.keyboards.product_inline import catalog_menu_button, CategoriesCBF, CategoriesPaginateCBF
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
    category_count = await Category.get_count(session)
    page = math.ceil(category_count / 8)
    if callback_data.current_page > page or callback_data.current_page < 1:
        callback_data.current_page = 1
        callback_data.slice = 0
    if callback_data.action == 'next':
        categories = await Category.get_slice(
            session=session, offset=callback_data.slice, limit=callback_data.slice + 8
        )
    elif callback_data.action == 'previous':
        categories = await Category.get_slice(
            session=session, offset=callback_data.slice, limit=callback_data.slice + 8)
    else:
        #exceptions
        pass
    keyboard = catalog_menu_button(categories, callback_data, page)
    callback_data.current_page += 1
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
