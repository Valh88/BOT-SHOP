from tgbot.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def _make_connection_string(config: Config, async_fallback=False) -> str:
    result = (
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}:"
        f"{config.db.port}/{config.db.database}"
    )
    if async_fallback:
        result += "?async_fallback=True"
    return result


async def create_db_session(config: Config) -> AsyncSession:
    engine = create_async_engine(
        _make_connection_string(config),
        future=True
    )

    async_session: AsyncSession = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session
