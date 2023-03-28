from typing import List, Union, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tgbot.models.products import Product


# async def get(
#         session: AsyncSession,
#         offset: Optional[int] = None,
#         limit: int = 10
# ):
#     pass


async def get_or_create(
        session: AsyncSession,
        name='123123'
) -> Product:
    to_db = select(Product).where(Product.name == name)
    product = await session.scalar(to_db)
    if product is None:
        product = Product(
            name=name,
        )
        session.add(product), await session.commit()
    return product


async def get(
        session: AsyncSession,
        name: str,
) -> bool:
    to_db = select(Product).where(Product.name == name)
    if await session.scalar(to_db):
        return True