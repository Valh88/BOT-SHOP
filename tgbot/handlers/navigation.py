from contextlib import suppress
from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram.filters import Text
from aiogram.exceptions import TelegramBadRequest
from tgbot.keyboards.inline import create_help_submenu, create_inline_menu, create_warranty_submenu, create_user_menu
from tgbot.models.users import User

router = Router()



@router.callback_query(Text('help'))
async def menu_callback(callback: CallbackQuery,):
    keyboard = create_help_submenu()
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text='**',
            reply_markup=keyboard,
        )
    await callback.answer()


@router.callback_query(Text('back'))
async def to_main_menu(callback: CallbackQuery,):
    keyboard = create_inline_menu()
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text='**',
            reply_markup=keyboard,
        )
    await callback.answer()


@router.callback_query(Text('warranty'),)
async def to_warranty_menu(
    callback: CallbackQuery,
):
    keyboard = create_warranty_submenu()
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text='**',
            reply_markup=keyboard,
        )
    await callback.answer()


@router.callback_query(Text('cabinet'))
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
