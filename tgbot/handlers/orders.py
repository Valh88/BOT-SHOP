import math
from contextlib import suppress
from typing import Optional
from aiogram import exceptions, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.keyboards.orders_inline import order_button, currencies_button, check_button, pay_button
from tgbot.keyboards.product_inline import ProductDetailCBF
from tgbot.models.products import Product
from tgbot.misc.states import OrderProductFSM
from tgbot.lexicon.lexicon import CURRENCIES
from tgbot.services.rocket_pay import rocket

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
                 f'цена {product.price} у.е.\n'
                 f'далее смотрим валюту!',
            reply_markup=currencies_button()
        )
    await state.set_state(OrderProductFSM.currency)


@router.callback_query(
    Text(list(CURRENCIES.keys())),
    StateFilter(OrderProductFSM.currency),
)
async def order_product(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    await state.update_data(currency=callback.data)
    data = await state.get_data()
    product = await Product.get_product_by_id(session, data['product_id'])
    with suppress(TelegramBadRequest):
        await callback.answer()
        await callback.message.edit_text(
            text=f'Товар: {product.name}, Описание {product.description},'
                 f'валюта{callback.data} '
                 f'цена {product.price}\n'
                 f'Для подтверждения нажмите "к оплате", либо в главное меню\n'
                 f'мы используем Рокету в качестве шлюза',
            reply_markup=check_button()
        )
    await state.set_state(OrderProductFSM.order)


@router.callback_query(
    Text('order'),
    StateFilter(OrderProductFSM.order),
)
async def order_product(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    product = await Product.get_product_by_id(session, data['product_id'])
    description = f"Покупка {product.name}, валюта: {data['currency']}"
    order = await rocket.create_invoice_tg(
        amount=product.price,
        currency=data['currency'],
        description=description,
        hidden_message="Спасибо за использование нашего сервиса",
        callback_url='https://t.me/btt14_88_bot',
        expired_in=86200
    )
    # order = {'success': True, 'data':
    #     {'description': 'Покупка name_4, валюта: SCALE', 'status': 'active', 'totalActivations': 1, 'activationsLeft': 1,
    #      'hiddenMessage': 'Спасибо за использование нашего сервиса', 'payload': None,
    #      'callbackUrl': 'https://t.me/btt14_88_bot', 'expiredIn': 86200, 'id': 2377, 'amount': 14888,
    #      'minPayment': None, 'currency': 'SCALE', 'link': 'https://t.me/ton_rocket_test_bot?start=inv_b329XTzf6XHKKA5'}}
    if order['success']:
        url = order['data']['link']
        with suppress(TelegramBadRequest):
            await callback.answer()
            await callback.message.edit_text(
                text=f'Товар: {product.name}, Описание {product.description},'
                     f'валюта: {data["currency"]} '
                     f'цена: {product.price}'
                     f'у.е.\n'
                     f'Вы будете перенаправлены на  платежный сервис',
                reply_markup=pay_button(url=url)
            )
    else:
        await callback.message.edit_text(
            text='ошибка')
    await state.clear()


# @router.message(Text('order'))
# async def catalog_menu(
#         message: Message,
#         request: ClientSession
# ):
#     # print(request)
#     data = await get_available_currencies(session=request)
#     await message.answer(
#         text='order',
#         # reply_markup=keyboard
#     )

