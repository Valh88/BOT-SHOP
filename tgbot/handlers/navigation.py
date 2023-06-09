from contextlib import suppress

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.exceptions import TelegramBadRequest
from tgbot.keyboards.inline import create_help_submenu, create_inline_menu, create_warranty_submenu, create_user_menu
from tgbot.models.users import User

router = Router()


@router.callback_query(Text('help'))
async def menu_callback(callback: CallbackQuery,):
    keyboard = create_help_submenu()
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text='Здесь вы можете узнать, что вам не понятно авыаыавыа',
            reply_markup=keyboard,
        )
    await callback.answer()


@router.callback_query(Text('back'))
async def to_main_menu(callback: CallbackQuery, state: FSMContext,):
    keyboard = create_inline_menu()
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text=f'Hello, Это тестовая  страничка. Это магазин для продажи 1111 123123',
            reply_markup=keyboard,
        )
    await state.clear()
    await callback.answer()


@router.callback_query(Text('warranty'),)
async def to_warranty_menu(
    callback: CallbackQuery,
):
    keyboard = create_warranty_submenu()
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text='Здесь можно связаться с администрацией и все такое',
            reply_markup=keyboard,
        )
    await callback.answer()


@router.callback_query(Text('profile'),)
async def to_cabinet_menu(
    callback: CallbackQuery,
    user: User,
):
    with suppress(TelegramBadRequest):
        keyboard = create_user_menu() 
        text = f'твой никнейм {user.username}, Тест'
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
    await callback.answer()


@router.message(Command('profile'))
async def to_warranty_menu(
    message: Message,
    user: User,
    state: FSMContext,
):
    keyboard = create_user_menu()
    text = f'твой никнейм {user.username}, Тест'
    await message.answer(
        text=text,
        reply_markup=keyboard,
    )
    await state.clear()
