from typing import Dict, List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.lexicon.lexicon import (
    INLINE_MENU,
    HELP_MENU,
    GARANTY_MENU,
    TO_MENU_BUTTON,
    ADMIN_BUTTON,
)

def create_inline_kb(
        button_data: Dict[str, str],
        width: int,
        *args: str,
        **kwargs: str,
) -> InlineKeyboardMarkup:

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=text[button] if button in button_data else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


def create_inline_menu() -> InlineKeyboardMarkup:
    kb_bulder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    button1: InlineKeyboardButton = InlineKeyboardButton(text=INLINE_MENU['vitrina'],
                                                         callback_data='vitrina',)
    button2 = InlineKeyboardButton(text=INLINE_MENU['bay'],
                                   callback_data='bay',)
    button3 = InlineKeyboardButton(text=INLINE_MENU['cabinet'],
                                   callback_data='cabinet',)
    button4 = InlineKeyboardButton(text=INLINE_MENU['help'],
                                   callback_data='help',)
    button5 = InlineKeyboardButton(text=INLINE_MENU['warranty'],
                                   callback_data='warranty',)
    button6 = InlineKeyboardButton(text=INLINE_MENU['fuck'],
                                   callback_data='fuck',)
    kb_bulder.row(button1, button2, width=1)
    kb_bulder.row(button3)
    kb_bulder.add(button4)
    kb_bulder.row(button5)
    kb_bulder.row(button6)

    return kb_bulder.as_markup()


def create_help_submenu() -> InlineKeyboardMarkup:
    kb_bulder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    [
        buttons.append(
            InlineKeyboardButton(text=value, callback_data=key)
        ) for key, value in HELP_MENU.items()
    ]

    kb_bulder.row(*buttons, width=1)
    kb_bulder.row(InlineKeyboardButton(text=TO_MENU_BUTTON['back'], callback_data='back'))
    return kb_bulder.as_markup()


def create_warranty_submenu():
    kb_bulder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    [
      buttons.append(InlineKeyboardButton(
        text=GARANTY_MENU[key],
        callback_data=key,)) for key in GARANTY_MENU.keys()
    ]
    kb_bulder.row(*buttons, width=1)
    kb_bulder.row(InlineKeyboardButton(text=TO_MENU_BUTTON['back'], callback_data='back'))
    return kb_bulder.as_markup()


def create_user_menu():
    kb_bulder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_bulder.row(InlineKeyboardButton(text=TO_MENU_BUTTON['back'], callback_data='back'))
    return kb_bulder.as_markup()


def create_admin_menu():
    kb_bulder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    [
        buttons.append(InlineKeyboardButton(
            text=ADMIN_BUTTON[key],
            callback_data=key,)) for key in ADMIN_BUTTON.keys()
    ]
    kb_bulder.row(*buttons)
    kb_bulder.row(InlineKeyboardButton(text=TO_MENU_BUTTON['back'], callback_data='back'))
    return kb_bulder.as_markup()
