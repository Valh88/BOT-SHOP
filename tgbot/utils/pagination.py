import math
from typing import Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.models import Product, Category


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

    async def get_list_models(self, offset, limit: int, session: AsyncSession):
        count = await self.model.get_count(session)
        page = math.ceil(count / limit)
        models = await self.model.get_slice(offset=offset, limit=limit, session=session)
        print(models, page)
        return

