from aiogram import Bot
from aiogram.types import BotCommand
from tgbot.lexicon.lexicon import MENU


async def main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in MENU.items()]
    await bot.set_my_commands(main_menu_commands)
