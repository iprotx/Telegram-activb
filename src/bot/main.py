import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import Settings
from bot.db.session import Database, create_database
from bot.middlewares import ErrorMiddleware, ServicesMiddleware
from bot.routers import router


def create_bot(settings: Settings) -> Bot:
    return Bot(token=settings.bot_token_value)


def create_dispatcher(database: Database) -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.update.outer_middleware(ErrorMiddleware())
    dispatcher.update.outer_middleware(ServicesMiddleware(database.session_factory))
    dispatcher.include_router(router)
    return dispatcher


async def run(settings: Settings) -> None:
    database = create_database(settings)
    try:
        async with create_bot(settings) as bot:
            dispatcher = create_dispatcher(database)
            await dispatcher.start_polling(bot)
    finally:
        await database.dispose()


def main() -> None:
    settings = Settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    asyncio.run(run(settings))


if __name__ == "__main__":
    main()
