import math
from contextlib import suppress
from typing import Optional
from aiogram import exceptions
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Text
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.models import Category
from tgbot.keyboards.product_inline import catalog_menu_button, CategoriesCBF, CategoriesPaginateCBF, \
    ProductsPaginateCBF, products_str_button, products_button, ProductsCatalogPaginateCBF
from tgbot.models.products import Product

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
    categories, page = await Category.get_list_models(
        session=session,
        callback_data=callback_data if callback_data else None
    )
    keyboard = catalog_menu_button(categories, callback_data, page)
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text='Это каталог. Щелкнуть на категорию, чтобы перейти на нужный продукт',
            reply_markup=keyboard
        )


@router.callback_query(CategoriesCBF.filter())
async def catalog_products(
        callback: CallbackQuery,
        callback_data: CategoriesCBF,
        session: AsyncSession,
):
    count = await Product.get_count_products_by_category(session=session, catalog_id=callback_data.category_id)
    products = await Product.get_slice_by_category_id(
        session=session, offset=0, limit=8, category_id=callback_data.category_id
    )
    if len(products) == 0:
        raise exceptions.CallbackAnswerException('пустая категория, такого не должно быть')
    await callback.message.edit_text(
        text=f'Категория: {callback_data.category_id}, чтобы перейти к нужному товару, жмякна кнопку '
             f'товарам которые нахотяся в этойкатегории',
        reply_markup=products_button(products=products, count=count)
    )


@router.callback_query(ProductsCatalogPaginateCBF.filter())
async def catalog_products(
        callback: CallbackQuery,
        callback_data: ProductsCatalogPaginateCBF,
        session: AsyncSession,
):
    category = callback_data.category_id
    products, page, callback_data = await Product.get_products_by_id_category(
        session=session,
        callback_data=callback_data
    )
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text=f'Категория: {category}, чтобы перейти к нужному товару, жмякна кнопку '
                 f'товарам которые нахотяся в этойкатегории',
            reply_markup=products_button(products=products, callback_data=callback_data, count=page)
        )


@router.callback_query(Text('list'))
async def products_list(
        callback: CallbackQuery,
        session: AsyncSession,
):
    products, page = await Product.get_str_product(session=session,)
    await callback.answer()
    await callback.message.edit_text(
        text=f'{products}',
        reply_markup=products_str_button(page)
    )


@router.callback_query(ProductsPaginateCBF.filter())
async def products_list(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: ProductsPaginateCBF
):
    products, page = await Product.get_str_product(
        session=session,
        callback_data=callback_data if callback_data else None,
    )
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text=f'{products}',
            reply_markup=products_str_button(callback_data=callback_data, count=page)
        )


@router.callback_query(Text('num'))
async def products_list(
        callback: CallbackQuery,

):
    await callback.answer()
