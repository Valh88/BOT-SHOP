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

    async def get_list_models(self, offset, limit: int, session: AsyncSession, callback_data):
        count = await self.model.get_count(session)
        page = math.ceil(count / limit)
        models = await self.model.get_slice(offset=offset, limit=limit, session=session)
        # print(models, page)

        if callback_data.current_page > page or callback_data.current_page < 1:
            callback_data.current_page = 1
            callback_data.slice = 0
        if callback_data.action == 'next':
            categories = await Category.get_slice(
                session=session, offset=callback_data.slice, limit=callback_data.slice + 8
            )
        elif callback_data.action == 'previous':
            categories = await Category.get_slice(
                session=session, offset=callback_data.slice, limit=callback_data.slice + 8)
        else:
            # exceptions
            pass
        return models

