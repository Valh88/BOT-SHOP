from typing import List, Union, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tgbot.models.products import Category
from aiogram.types import User as TelegramUser


async def get_or_create(
        session: AsyncSession,
        name: str,
) -> Category:
    to_db = select(Category).where(Category.name == name)
    category = await session.scalar(to_db)
    if category is None:
        category = Category(
            name=name,
        )
        session.add(category), await session.commit()
    return category


async def get(
        session: AsyncSession,
        name: Optional[str] = None,
) -> Union[Category, List[Category]]:
    if name:
        to_db = select(Category).where(Category.name == name)
        category = await session.scalar(to_db)
        return category
    categories = await session.execute(select(Category))
    return categories.scalars().all()


# async def get_all(
#         session: AsyncSession,
# ) -> List[Category]:
