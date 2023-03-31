import math
from typing import Union, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.models import Product, Category
from tgbot.keyboards.product_inline import CategoriesPaginateCBF


class Page:
    def __init__(
            self,
            models: Union[List[Category], List[Product]],
            count: int,
            num_page: int,
    ):
        pass


class Paginator:
    def __init__(
            self, model: Union[Category, Product],
    ):
        self.model = model

    async def get_list_models(
            self,
            session: AsyncSession,
            callback_data: CategoriesPaginateCBF,
    ) -> Tuple[List[Category], CategoriesPaginateCBF, int]:
        count = await self.model.get_count(session)
        page = math.ceil(count / 8)
        if callback_data.current_page > page or callback_data.current_page < 1:
            callback_data.current_page = 1
            callback_data.slice = 0
        models = await self.model.get_slice(
            session=session, offset=callback_data.slice, limit=callback_data.slice + 8)
        return models, callback_data, page

