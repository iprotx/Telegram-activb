import asyncio
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.base import Base
from bot.db.models import User
from bot.repositories.users import UserRepository


async def test_user_repository_registration_is_idempotent_across_sessions(tmp_path: Path) -> None:
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'users.db'}"
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as first_session:
        first_user = await UserRepository(first_session).get_or_create(
            telegram_id=42,
            username="alice",
            first_name="Alice",
            last_name="Smith",
        )
        await first_session.commit()

    async with session_factory() as second_session:
        second_user = await UserRepository(second_session).get_or_create(
            telegram_id=42,
            username="alice-new",
            first_name="Alice New",
            last_name=None,
        )
        await second_session.commit()

    assert second_user.id == first_user.id
    assert second_user.username == "alice-new"
    assert second_user.first_name == "Alice New"
    assert second_user.last_name is None

    await engine.dispose()


async def test_user_repository_concurrent_registration_creates_one_user(tmp_path: Path) -> None:
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'concurrent.db'}"
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    barrier = asyncio.Barrier(2)

    async def register(username: str) -> int:
        async with session_factory() as session:
            await barrier.wait()
            user = await UserRepository(session).get_or_create(
                telegram_id=99,
                username=username,
                first_name="Concurrent",
                last_name=None,
            )
            await session.commit()
            return user.id

    first_id, second_id = await asyncio.gather(register("first"), register("second"))

    async with session_factory() as session:
        count = await session.scalar(
            select(func.count()).select_from(User).where(User.telegram_id == 99)
        )

    assert count == 1
    assert first_id == second_id

    await engine.dispose()
