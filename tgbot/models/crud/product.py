from typing import List, Union, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tgbot.models.products import Product


async def get(
        session: AsyncSession,
        offset: Optional[int] = None,
        limit: int = 10
):
    pass
