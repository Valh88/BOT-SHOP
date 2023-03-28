from aiogram.filters.state import State, StatesGroup


class NewCategoryFSM(StatesGroup):
    category = State()


class ProductFSM(StatesGroup):
    name = State()
    count = State()
    category = State()
    description = State()
    picture = State()
