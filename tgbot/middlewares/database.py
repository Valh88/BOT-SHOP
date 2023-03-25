from typing import Callable, Any, Awaitable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from tgbot.models.crud.user import current_user


class DbMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        self.session_pool = session_pool

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]],
                                         Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        async with self.session_pool() as session:
            data['session'] = session

            user = await current_user(session=session, user=event.from_user)
            data['user'] = user
            result = await handler(event, data)
        return result
