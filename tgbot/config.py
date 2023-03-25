from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    port: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def settings(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            port=env.str('DB_PORT'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
        ),
        misc=Miscellaneous()
    )


config = settings()

RATE_LIMIT: float = 2.0
