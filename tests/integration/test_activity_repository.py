import asyncio
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.base import Base
from bot.db.models import Chat, ChatMember, User
from bot.repositories.activity import ActivityRepository
from bot.services.activity_tracking import ActivityService


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
        member = await ActivityService(ActivityRepository(session)).record_message(
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
        member = await ActivityService(ActivityRepository(session)).record_message(
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
        member = await ActivityService(ActivityRepository(session)).record_message(
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
        member = await ActivityService(ActivityRepository(session)).record_message(
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


async def test_rank_is_scoped_to_chat_and_orders_ties_deterministically(tmp_path: Path) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'rank.db'}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        first_user = User(
            telegram_id=710_001,
            username="first-user",
            first_name="First",
            last_name=None,
        )
        second_user = User(
            telegram_id=710_002,
            username="second-user",
            first_name="Second",
            last_name=None,
        )
        third_user = User(
            telegram_id=710_003,
            username="third-user",
            first_name="Third",
            last_name=None,
        )
        first_chat = Chat(telegram_id=-710_001, title="First chat")
        other_chat = Chat(telegram_id=-710_002, title="Other chat")
        session.add_all([first_user, second_user, third_user, first_chat, other_chat])
        await session.flush()
        session.add_all(
            [
                ChatMember(
                    chat_id=first_chat.id,
                    user_id=first_user.id,
                    xp=200,
                    level=2,
                    message_count=5,
                ),
                ChatMember(
                    chat_id=first_chat.id,
                    user_id=second_user.id,
                    xp=200,
                    level=2,
                    message_count=10,
                ),
                ChatMember(
                    chat_id=first_chat.id,
                    user_id=third_user.id,
                    xp=100,
                    level=2,
                    message_count=30,
                ),
                ChatMember(
                    chat_id=other_chat.id,
                    user_id=first_user.id,
                    xp=900,
                    level=4,
                    message_count=40,
                ),
            ]
        )
        await session.commit()

        repository = ActivityRepository(session)
        first_rank = await repository.get_member_rank(
            chat_telegram_id=-710_001,
            user_telegram_id=710_001,
        )
        username_rank = await repository.get_member_rank(
            chat_telegram_id=-710_001,
            username="THIRD-USER",
        )
        other_chat_rank = await repository.get_member_rank(
            chat_telegram_id=-710_002,
            user_telegram_id=710_001,
        )
        unknown_rank = await repository.get_member_rank(
            chat_telegram_id=-710_001,
            username="unknown-user",
        )

        assert first_rank is not None
        assert (first_rank[0].xp, first_rank[2]) == (200, 2)
        assert username_rank is not None
        assert (username_rank[1].username, username_rank[2]) == ("third-user", 3)
        assert other_chat_rank is not None
        assert (other_chat_rank[0].xp, other_chat_rank[2]) == (900, 1)
        assert unknown_rank is None

    await engine.dispose()


async def test_top_members_is_chat_scoped_ordered_and_limited(tmp_path: Path) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'top.db'}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        users = [
            User(
                telegram_id=720_001,
                username="top-first",
                first_name="First",
                last_name=None,
            ),
            User(
                telegram_id=720_002,
                username="top-second",
                first_name="Second",
                last_name=None,
            ),
            User(
                telegram_id=720_003,
                username="top-third",
                first_name="Third",
                last_name=None,
            ),
        ]
        first_chat = Chat(telegram_id=-720_001, title="First chat")
        other_chat = Chat(telegram_id=-720_002, title="Other chat")
        session.add_all([*users, first_chat, other_chat])
        await session.flush()
        session.add_all(
            [
                ChatMember(
                    chat_id=first_chat.id,
                    user_id=users[0].id,
                    xp=100,
                    level=2,
                    message_count=3,
                ),
                ChatMember(
                    chat_id=first_chat.id,
                    user_id=users[1].id,
                    xp=300,
                    level=2,
                    message_count=5,
                ),
                ChatMember(
                    chat_id=first_chat.id,
                    user_id=users[2].id,
                    xp=200,
                    level=2,
                    message_count=4,
                ),
                ChatMember(
                    chat_id=other_chat.id,
                    user_id=users[0].id,
                    xp=900,
                    level=4,
                    message_count=10,
                ),
            ]
        )
        await session.commit()

        repository = ActivityRepository(session)
        top = await repository.get_top_members(chat_telegram_id=-720_001, limit=2)
        assert [(user.username, member.xp) for member, user in top] == [
            ("top-second", 300),
            ("top-third", 200),
        ]
        other_top = await repository.get_top_members(chat_telegram_id=-720_002)
        assert [(user.username, member.xp) for member, user in other_top] == [
            ("top-first", 900)
        ]

    await engine.dispose()


@pytest.mark.skipif(
    not os.getenv("DATABASE_URL"),
    reason="requires PostgreSQL integration database",
)
async def test_concurrent_first_messages_are_serialized() -> None:
    database_url = os.environ["DATABASE_URL"]
    if not database_url.startswith("postgresql+asyncpg://"):
        pytest.fail("DATABASE_URL must use PostgreSQL asyncpg for this integration test")

    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    unique_id = uuid4().int % (2**62)
    user_telegram_id = unique_id + 1
    chat_telegram_id = -(unique_id + 1)
    now = datetime(2026, 1, 1, tzinfo=UTC)

    async with session_factory() as session:
        user = User(
            telegram_id=user_telegram_id,
            username="concurrent-activity-test",
            first_name="Concurrent",
            last_name="Activity",
        )
        session.add(user)
        await session.commit()
        user_id = user.id

    barrier = asyncio.Barrier(2)

    async def record(message_id: int) -> None:
        async with session_factory() as session:
            user = await session.get(User, user_id)
            assert user is not None
            await barrier.wait()
            await ActivityService(ActivityRepository(session)).record_message(
                chat_telegram_id=chat_telegram_id,
                chat_title="Concurrent activity test",
                user=user,
                message_id=message_id,
                now=now,
            )
            await session.commit()

    await asyncio.gather(record(101), record(102))

    async with session_factory() as session:
        member = await session.scalar(select(ChatMember).where(ChatMember.user_id == user_id))
        assert member is not None
        assert member.message_count == 2
        # Both messages share a timestamp, so cooldown should allow only one XP award.
        assert member.xp == 10

    await engine.dispose()
