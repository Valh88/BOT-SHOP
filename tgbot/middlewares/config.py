from typing import Callable, Any, Awaitable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.crud.user import current_user


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config) -> None:
        self.config = config

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]],
                                         Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        data['config'] = self.config
        return await handler(event, data)


class CurrentUserMiddleware(BaseMiddleware):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]],
                                         Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        user = event.from_user
        user = current_user(user=user, session=self.session)
        data['current_user'] = user
        return await handler(event, data)
