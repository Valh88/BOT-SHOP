from aiogram import Router
from aiogram.types import Message

router: Router = Router()


@router.message()
async def send_echo(message: Message):
    # print(message.json(exclude_none=True, indent=4))

    await message.answer(f'Это эхо! {message.text}')

