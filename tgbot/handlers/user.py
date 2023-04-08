from contextlib import suppress

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.users import User
from tgbot.keyboards.inline import create_inline_menu

router = Router()


@router.message(CommandStart())
async def start_command(message: Message,
                        session: AsyncSession,
                        state: FSMContext,
                        user: User, bot):
    keyboard = create_inline_menu()
    await message.answer(
        text=f'Hello,{user.username}.  тест. Это магазин для продажи 1111 123123',
        reply_markup=keyboard,
    )
    await state.clear()


@router.callback_query(Text(['fuck', 'bay']))
async def menu_callback(callback: CallbackQuery,):
    data = callback.data
    if data in ['fuck', 'bay', 'profile']:
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                text=f'{data}- это в разработке',
                reply_markup=create_inline_menu(),
            )
        await callback.answer()

