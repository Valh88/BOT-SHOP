from aiogram.filters.state import State, StatesGroup


class NewCategoryFSM(StatesGroup):
    category = State()


class ProductFSM(StatesGroup):
    name = State()
    count = State()
    price = State()
    category = State()
    description = State()
    picture = State()


class OrderProductFSM(StatesGroup):
    product_id = State()
    count = State()
    currency = State()
    order = State()
