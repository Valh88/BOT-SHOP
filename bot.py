import asyncio
from sys import stderr
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import ClientSession
from tgbot.handlers import user, echo, navigation, admin, product, orders
from tgbot.config import config, Config
from tgbot.models.database import create_db_session
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DbMiddleware, SessionRequestMiddleware
from tgbot.middlewares.throttilng import ThrottlingMiddleware
from tgbot.keyboards.main_menu import main_menu

logger = logging.getLogger(__name__)


def register_global_middleware(dp: Dispatcher, config: Config, session_pool):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    dp.message.outer_middleware(DbMiddleware(session_pool))
    dp.callback_query.outer_middleware(DbMiddleware(session_pool))

    dp.message.outer_middleware(SessionRequestMiddleware(ClientSession()))
    dp.callback_query.outer_middleware(SessionRequestMiddleware(ClientSession()))

    dp.message.middleware(ThrottlingMiddleware())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info("Starting bot")

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    await main_menu(bot)

    if config.tg_bot.use_redis:
        redis: Redis = Redis()
        storage: RedisStorage = RedisStorage(redis=redis)
    else:
        storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    session_pool = await create_db_session(config)
    register_global_middleware(dp, config, session_pool)

    dp.include_router(user.router)
    dp.include_router(admin.router)
    dp.include_router(navigation.router)
    dp.include_router(product.router)
    dp.include_router(orders.router)
    # start
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

        # await bot.set_webhook(
        #     url=config.web_hook.web_hook_domain + config.web_hook.web_hook_path,
        #     drop_pending_updates=True,
        #     allowed_updates=dp.resolve_used_update_types()
        # )
        # app = web.Application()
        # SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.web_hook.web_hook_path)
        # runner = web.AppRunner(app)
        # await runner.setup()
        # site = web.TCPSite(runner, host='0.0.0.0', port=9000)
        # await site.start()

    finally:
        await dp.storage.close()
        # await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
