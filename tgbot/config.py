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
class WebHook:
    web_hook_domain: str
    web_hook_path: str


@dataclass
class Config:
    debug: bool
    rocket_pay_test: str
    tg_bot: TgBot
    db: DbConfig
    web_hook: WebHook


def settings(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        debug=env.str("DEBUG"),
        rocket_pay_test=env.str("ROCKET_PAY_TEST"),
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
        web_hook=WebHook(
            web_hook_domain=env.str('WEBHOOK_DOMAIN'),
            web_hook_path=env.str('WEBHOOK_PATH'),
        )
    )


config = settings()

RATE_LIMIT: float = 2.0
