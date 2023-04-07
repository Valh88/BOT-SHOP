import math
from contextlib import suppress
from typing import Optional
from aiogram import exceptions
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.exceptions import TelegramBadRequest
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.keyboards.orders_inline import order_button, currencies_button
from tgbot.models.models import Category
from tgbot.keyboards.product_inline import ProductDetailCBF
from tgbot.services.rocket_pay.rocket import get_available_currencies
from tgbot.models.products import Product
from tgbot.misc.states import OrderProductFSM
router = Router()


@router.callback_query(ProductDetailCBF.filter(),
                       StateFilter(default_state),
                       )
async def catalog_products(
        callback: CallbackQuery,
        callback_data: ProductDetailCBF,
        session: AsyncSession,
        state: FSMContext,
):
    product = await Product.get_product_by_id(session, callback_data.product_id)
    print(callback_data)
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text=f'Товар: {product.name}, Описание{product.description},'
                 f'цена 1488 у.е.\n'
                 f'Чтобы оформить заказ щелкните на кнопку ниже',
            reply_markup=order_button(product_id=product.id)
        )
    await state.set_state(OrderProductFSM.product_id)


@router.callback_query(
    StateFilter(OrderProductFSM.product_id),
    ProductDetailCBF.filter(),
)
async def order_product(
        callback: CallbackQuery,
        callback_data: ProductDetailCBF,
        state: FSMContext,
        session: AsyncSession,
):
    await state.update_data(product_id=callback_data.product_id)
    product = await Product.get_product_by_id(session, callback_data.product_id)
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text=f'Товар: {product.name}, Описание {product.description},'
                 f'цена 1488 у.е.\n'
                 f'далее смотрим валюту!',
            reply_markup=currencies_button()
        )
    await state.set_state(OrderProductFSM.currency)


@router.message(Text('order'))
async def catalog_menu(
        message: Message,
        request: ClientSession
):
    # print(request)
    data = await get_available_currencies(session=request)
    await message.answer(
        text='order',
        # reply_markup=keyboard
    )

