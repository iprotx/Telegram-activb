import os

import pytest
from aiogram.types import Update
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.models import User
from bot.middlewares.services import ServicesMiddleware


@pytest.mark.skipif(
    not os.getenv("DATABASE_URL"),
    reason="requires PostgreSQL integration database",
)
async def test_services_middleware_rolls_back_failed_handler() -> None:
    database_url = os.environ["DATABASE_URL"]
    if not database_url.startswith("postgresql+asyncpg://"):
        pytest.fail("DATABASE_URL must use PostgreSQL asyncpg for this integration test")

    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def handler(event: Update, data: dict[str, object]) -> None:
        service = data["user_service"]
        await service.register(telegram_id=123, username="rollback")  # type: ignore[union-attr]
        raise RuntimeError("handler failed")

    middleware = ServicesMiddleware(session_factory)

    with pytest.raises(RuntimeError, match="handler failed"):
        await middleware(handler, Update(update_id=1), {})

    async with session_factory() as session:
        count = await session.scalar(
            select(func.count()).select_from(User).where(User.telegram_id == 123)
        )

    assert count == 0

    await engine.dispose()
