from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.base import Base
from bot.repositories.users import UserRepository


async def test_user_repository_creates_and_reads_user() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        repository = UserRepository(session)
        user = await repository.get_or_create(telegram_id=42, username="alice")

        assert user.telegram_id == 42
        assert user.username == "alice"

        same_user = await repository.get_or_create(telegram_id=42, username="alice-2")
        assert same_user.id == user.id

    await engine.dispose()
