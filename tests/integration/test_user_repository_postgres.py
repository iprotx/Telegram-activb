import asyncio
import os

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.models import User
from bot.repositories.users import UserRepository


pytestmark = pytest.mark.postgres


def _database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if os.getenv("CI") != "true":
        pytest.skip("PostgreSQL integration tests run in CI")
    if not database_url or not database_url.startswith("postgresql+asyncpg://"):
        pytest.fail("CI PostgreSQL integration tests require a postgresql+asyncpg DATABASE_URL")
    return database_url


async def test_user_schema_allows_nullable_profile_fields_and_enforces_unique_telegram_id() -> None:
    engine = create_async_engine(_database_url())
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        first_user = User(telegram_id=-910000000001, username=None, first_name=None, last_name=None)
        session.add(first_user)
        await session.commit()

    async with session_factory() as session:
        duplicate = User(telegram_id=-910000000001, username="duplicate")
        session.add(duplicate)
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()

    await engine.dispose()


async def test_user_repository_concurrent_registration_creates_one_user() -> None:
    engine = create_async_engine(_database_url())
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    barrier = asyncio.Barrier(2)
    telegram_id = -910000000002

    async def register(username: str) -> int:
        async with session_factory() as session:
            await barrier.wait()
            user = await UserRepository(session).get_or_create(
                telegram_id=telegram_id,
                username=username,
                first_name="Concurrent",
                last_name=None,
            )
            await session.commit()
            return user.id

    first_id, second_id = await asyncio.gather(register("first"), register("second"))

    async with session_factory() as session:
        count = await session.scalar(
            select(func.count()).select_from(User).where(User.telegram_id == telegram_id)
        )

    assert count == 1
    assert first_id == second_id

    await engine.dispose()
