from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.base import Base
from bot.repositories.users import UserRepository


async def test_user_repository_creates_and_synchronizes_user_profile() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        repository = UserRepository(session)
        user = await repository.get_or_create(
            telegram_id=42,
            username="alice",
            first_name="Alice",
            last_name="Smith",
        )

        assert user.telegram_id == 42
        assert user.username == "alice"
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"

        same_user = await repository.get_or_create(
            telegram_id=42,
            username="alice-new",
            first_name="Alice New",
            last_name=None,
        )
        assert same_user.id == user.id
        assert same_user.username == "alice-new"
        assert same_user.first_name == "Alice New"
        assert same_user.last_name is None

    await engine.dispose()
