from typing import cast

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from bot.db.session import Database


class FakeEngine:
    def __init__(self) -> None:
        self.dispose_calls = 0

    async def dispose(self) -> None:
        self.dispose_calls += 1


async def test_database_disposes_engine() -> None:
    engine = FakeEngine()
    database = Database(
        engine=cast(AsyncEngine, engine),
        session_factory=cast(async_sessionmaker[AsyncSession], object()),
    )

    await database.dispose()

    assert engine.dispose_calls == 1
