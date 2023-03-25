from typing import Dict, List
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tgbot.lexicon.lexicon import INLINE_MENU, BUTTON_ARGS, HELP_MENU, GARANTY_MENU


def create_reply_menu() -> ReplyKeyboardBuilder:
    
    kb_bulder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    # buttons = list[InlineKeyboardButton] = []

    button1: KeyboardButton = KeyboardButton(
        text=INLINE_MENU['vitrina'],
    )
    button2: KeyboardButton =  KeyboardButton(
        text=INLINE_MENU['bay'],
    )

    button3: KeyboardButton = KeyboardButton(
        text=INLINE_MENU['cabinet'],
    )
    button4: KeyboardButton = KeyboardButton(
        text=INLINE_MENU['help'],

    )
    button5: KeyboardButton = KeyboardButton(
        text=INLINE_MENU['garanty'],
    )
    button6: KeyboardButton = KeyboardButton(
        text=INLINE_MENU['fuck'],
    )
    kb_bulder.row(button1, button2, width=1)
    kb_bulder.row(button3)
    kb_bulder.add(button4)
    kb_bulder.row(button5)
    kb_bulder.row(button6)

    return kb_bulder.as_markup()