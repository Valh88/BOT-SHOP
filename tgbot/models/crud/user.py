from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tgbot.models.user import User
from aiogram.types import User as TelegramUser


async def current_user(
        session: AsyncSession,
        user: TelegramUser,
) -> User:
    to_db = select(User).where(User.telega_id == user.id)
    current_user = await session.scalar(to_db)
    if current_user is None:
        current_user = User(
            telega_id=user.id,
            username=user.username,
            first_name=user.first_name,
            language_code=user.language_code,
            is_bot=user.is_bot,
        )
        session.add(current_user), await session.commit()
    return current_user
