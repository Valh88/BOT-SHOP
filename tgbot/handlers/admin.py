from contextlib import suppress
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram import Router, Bot, F
from aiogram.filters import Text, Command, StateFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import default_state
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.users import User
from tgbot.keyboards.inline import create_admin_menu
from tgbot.misc.states import NewCategoryFSM, ProductFSM
from tgbot.filters.admin import IsAdmin
from tgbot.config import config
from tgbot.models.crud import category
router = Router()


@router.message(Command(commands=['admin']), IsAdmin(admin_ids=config.tg_bot.admin_ids),)
async def admin_menu(message: Message,
                     user: User,
                     state: FSMContext):
    keyboard = create_admin_menu()
    await state.clear()
    await message.answer(
        text=f'Это админка {user.username}.',
        reply_markup=keyboard,
    )


@router.callback_query(Text(['category']),
                       IsAdmin(admin_ids=config.tg_bot.admin_ids),
                       StateFilter(default_state),)
async def add_new_product(
        callback: CallbackQuery,
        state: FSMContext,
):
    await callback.message.edit_text(
        text='введи название категории'
    )
    await state.set_state(NewCategoryFSM.category)


@router.message(IsAdmin(admin_ids=config.tg_bot.admin_ids),
                StateFilter(NewCategoryFSM.category),
                F.text.isalpha(),)
async def process_name_sent(
        message: Message,
        state: FSMContext,
        session: AsyncSession,):
    if await category.get(session, message.text):
        await message.answer(
            text='такая категория есть',
        )
        await state.set_state(NewCategoryFSM.category)
    else:
        cat = await category.get_or_create(session, message.text)
        await message.answer(
            text=f'Новая категория - {cat.name}'
        )
        await state.clear()


@router.callback_query(IsAdmin(admin_ids=config.tg_bot.admin_ids),
                       Text(['new_product']),
                       StateFilter(default_state),)
async def add_new_product(
        callback: CallbackQuery,
        state: FSMContext,
):
    await callback.message.edit_text(
        text='Добавляем новый товар 4 шага.\n '
             'Шаг 1.Введите название:'
    )
    await state.set_state(ProductFSM.name)


@router.message(IsAdmin(admin_ids=config.tg_bot.admin_ids),
                StateFilter(ProductFSM.name),
                F.text.isalpha(),)
async def add_new_product(
        message: Message,
        state: FSMContext,
):
    await state.update_data(name=message.text)
    await message.answer(
        text='Добавляем новый товар 4 шага.\n '
             'Шаг 2. Количество:'
    )
    await state.set_state(ProductFSM.count)


@router.message(IsAdmin(admin_ids=config.tg_bot.admin_ids),
                StateFilter(ProductFSM.count),
                F.text.isdigit(),)
async def add_new_product(
        message: Message,
        state: FSMContext,
):
    await state.update_data(count=message.text)
    await message.answer(
        text='Добавляем новый товар 4 шага.\n '
             'Шаг 3. Описание:'
    )
    await state.set_state(ProductFSM.description)


@router.message(IsAdmin(admin_ids=config.tg_bot.admin_ids),
                StateFilter(ProductFSM.description),
                F.text.isalpha(),)
async def add_new_product(
        message: Message,
        state: FSMContext,
):
    await state.update_data(description=message.text)
    await message.answer(
        text='Добавляем новый товар 4 шага.\n '
             'Шаг 4. Пикча:'
    )
    await state.set_state(ProductFSM.picture)


@router.message(IsAdmin(admin_ids=config.tg_bot.admin_ids),
                StateFilter(ProductFSM.picture),
                F.content_type == ContentType.PHOTO)
async def add_new_product(
        message: Message,
        state: FSMContext,
        bot: Bot,
):
    # print(message.json(exclude_none=True, indent=4))
    photo = message.photo[-1]
    # await bot.download(photo.file_id, destination=f'./media/{photo.file_id}.jpg')
    data = await state.get_data()
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=photo.file_id,
                         caption=f'Описание: {data["description"]}\n'
                                 f'Количество: {data["count"]}')
    await state.clear()
