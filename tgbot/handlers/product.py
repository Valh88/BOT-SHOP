from contextlib import suppress
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Text
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.crud import category
from tgbot.keyboards.inline import button_back
from tgbot.keyboards.product_inline import catalog_menu_button, CategoriesCBF

router = Router()


@router.callback_query(Text('vitrina'))
async def catalog_menu(
        callback: CallbackQuery,
        session: AsyncSession,
):
    categories = await category.get(session)
    keyboard = catalog_menu_button(categories)
    await callback.message.edit_text(
        text='123',
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
