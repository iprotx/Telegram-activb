import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import Settings
from bot.db.session import create_session_factory
from bot.middlewares import ErrorMiddleware, ServicesMiddleware
from bot.routers import router


def create_bot(settings: Settings) -> Bot:
    return Bot(token=settings.bot_token_value)


def create_dispatcher(settings: Settings) -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.update.outer_middleware(ErrorMiddleware())
    dispatcher.update.outer_middleware(ServicesMiddleware(create_session_factory(settings)))
    dispatcher.include_router(router)
    return dispatcher


async def run(settings: Settings) -> None:
    bot = create_bot(settings)
    dispatcher = create_dispatcher(settings)
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


def main() -> None:
    settings = Settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    asyncio.run(run(settings))


if __name__ == "__main__":
    main()
