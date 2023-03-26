from contextlib import suppress
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.users import User
from tgbot.keyboards.inline import create_inline_menu
from tgbot.config import config
router = Router()


@router.message(CommandStart())
async def start_command(message: Message,
                        session: AsyncSession,
                        user: User, bot):
    keyboard = create_inline_menu()
    await message.answer(
        text=f'Hello,{user.username}.  тест',
        reply_markup=keyboard,
    )


@router.callback_query(Text(['vitrina', 'fuck', 'bay']))
async def menu_callback(callback: CallbackQuery,):
    data = callback.data
    if data in ['vitrina', 'fuck', 'bay', 'cabinet']:
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                text=f'{data}- это в разработке',
                reply_markup=create_inline_menu(),
            )
        await callback.answer()

