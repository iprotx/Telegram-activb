from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.base import Base
from bot.db.models import ChatMember, User
from bot.repositories.activity import ActivityRepository


async def test_activity_records_messages_idempotently_and_respects_cooldown(
    tmp_path: Path,
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'activity.db'}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    now = datetime(2026, 1, 1, tzinfo=UTC)
    async with session_factory() as session:
        user = User(
            telegram_id=700_001,
            username="activity-test",
            first_name="Activity",
            last_name="Test",
        )
        session.add(user)
        await session.commit()
        user_id = user.id

    async with session_factory() as session:
        user = await session.get(User, user_id)
        assert user is not None
        member = await ActivityRepository(session).record_message(
            chat_telegram_id=-700_001,
            chat_title="Activity test",
            user=user,
            message_id=1,
            now=now,
        )
        assert (member.message_count, member.xp, member.level) == (1, 10, 1)
        await session.commit()

    # A replayed Telegram message must not increment count or award XP twice.
    async with session_factory() as session:
        user = await session.get(User, user_id)
        assert user is not None
        member = await ActivityRepository(session).record_message(
            chat_telegram_id=-700_001,
            chat_title="Activity test",
            user=user,
            message_id=1,
            now=now + timedelta(seconds=5),
        )
        assert (member.message_count, member.xp) == (1, 10)
        await session.commit()

    # The timestamp loaded back from SQLite is naive; policy must still compare it safely.
    async with session_factory() as session:
        user = await session.get(User, user_id)
        assert user is not None
        member = await ActivityRepository(session).record_message(
            chat_telegram_id=-700_001,
            chat_title="Activity test",
            user=user,
            message_id=2,
            now=now + timedelta(seconds=30),
        )
        assert (member.message_count, member.xp) == (2, 10)
        await session.commit()

    async with session_factory() as session:
        user = await session.get(User, user_id)
        assert user is not None
        member = await ActivityRepository(session).record_message(
            chat_telegram_id=-700_001,
            chat_title="Activity test",
            user=user,
            message_id=3,
            now=now + timedelta(seconds=60),
        )
        assert (member.message_count, member.xp) == (3, 20)
        await session.commit()

    async with session_factory() as session:
        member = await session.scalar(select(ChatMember).where(ChatMember.user_id == user_id))
        assert member is not None
        assert (member.message_count, member.xp, member.level) == (3, 20, 1)

    await engine.dispose()
