from datetime import UTC, datetime, timedelta
from typing import Any

from bot.db.models import ChatMember, User
from bot.services.activity_tracking import ActivityService


class FakeActivityRepository:
    def __init__(self, member: ChatMember, *, duplicate: bool = False) -> None:
        self.member = member
        self.duplicate = duplicate
        self.prepared: list[dict[str, Any]] = []
        self.recorded: list[dict[str, Any]] = []
        self.rank_result: tuple[ChatMember, User, int] | None = None
        self.rank_lookup: dict[str, Any] | None = None
        self.top_result: list[tuple[ChatMember, User]] = []
        self.top_lookup: dict[str, Any] | None = None

    async def get_member_rank(
        self,
        *,
        chat_telegram_id: int,
        user_telegram_id: int | None = None,
        username: str | None = None,
    ) -> tuple[ChatMember, User, int] | None:
        self.rank_lookup = {
            "chat_telegram_id": chat_telegram_id,
            "user_telegram_id": user_telegram_id,
            "username": username,
        }
        return self.rank_result

    async def get_top_members(
        self,
        *,
        chat_telegram_id: int,
        limit: int = 10,
    ) -> list[tuple[ChatMember, User]]:
        self.top_lookup = {"chat_telegram_id": chat_telegram_id, "limit": limit}
        return self.top_result

    async def prepare_message(
        self,
        *,
        chat_telegram_id: int,
        chat_title: str | None,
        user: User,
        message_id: int,
    ) -> tuple[ChatMember, bool]:
        self.prepared.append(
            {
                "chat_telegram_id": chat_telegram_id,
                "chat_title": chat_title,
                "user": user,
                "message_id": message_id,
            }
        )
        return self.member, self.duplicate

    async def record_message(
        self,
        *,
        member: ChatMember,
        message_id: int,
        xp_awarded: int,
        new_level: int,
        now: datetime,
    ) -> ChatMember:
        self.recorded.append(
            {
                "member": member,
                "message_id": message_id,
                "xp_awarded": xp_awarded,
                "new_level": new_level,
                "now": now,
            }
        )
        member.message_count += 1
        member.xp += xp_awarded
        member.level = new_level
        if xp_awarded:
            member.last_xp_at = now
        return member


def make_member(*, xp: int = 0, level: int = 1, last_xp_at: datetime | None = None) -> ChatMember:
    return ChatMember(
        id=1,
        chat_id=10,
        user_id=20,
        xp=xp,
        level=level,
        message_count=0,
        last_xp_at=last_xp_at,
    )


def make_user() -> User:
    return User(
        id=20,
        telegram_id=200,
        username="test-user",
        first_name="Test",
        last_name=None,
    )


async def test_activity_service_decides_xp_and_level_before_persistence() -> None:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    member = make_member(xp=90)
    repository = FakeActivityRepository(member)
    service = ActivityService(repository)  # type: ignore[arg-type]

    result = await service.record_message(
        chat_telegram_id=-100,
        chat_title="Test chat",
        user=make_user(),
        message_id=55,
        now=now,
    )

    assert result.xp == 100
    assert result.level == 2
    assert result.message_count == 1
    assert repository.recorded == [
        {
            "member": member,
            "message_id": 55,
            "xp_awarded": 10,
            "new_level": 2,
            "now": now,
        }
    ]


async def test_activity_service_applies_cooldown_outside_repository() -> None:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    member = make_member(xp=100, level=2, last_xp_at=now - timedelta(seconds=30))
    repository = FakeActivityRepository(member)
    service = ActivityService(repository)  # type: ignore[arg-type]

    result = await service.record_message(
        chat_telegram_id=-100,
        chat_title="Test chat",
        user=make_user(),
        message_id=56,
        now=now,
    )

    assert result.xp == 100
    assert result.level == 2
    assert repository.recorded[0]["xp_awarded"] == 0
    assert repository.recorded[0]["new_level"] == 2


async def test_activity_service_does_not_persist_duplicate_message() -> None:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    member = make_member(xp=10, level=1, last_xp_at=now - timedelta(seconds=5))
    repository = FakeActivityRepository(member, duplicate=True)
    service = ActivityService(repository)  # type: ignore[arg-type]

    result = await service.record_message(
        chat_telegram_id=-100,
        chat_title="Test chat",
        user=make_user(),
        message_id=55,
        now=now,
    )

    assert result is member
    assert result.message_count == 0
    assert repository.recorded == []


async def test_activity_service_looks_up_rank_in_the_requested_chat() -> None:
    member = make_member(xp=250, level=2)
    user = make_user()
    repository = FakeActivityRepository(member)
    repository.rank_result = (member, user, 3)
    service = ActivityService(repository)  # type: ignore[arg-type]

    result = await service.get_member_rank(chat_telegram_id=-100, username="test-user")

    assert result == (member, user, 3)
    assert repository.rank_lookup == {
        "chat_telegram_id": -100,
        "user_telegram_id": None,
        "username": "test-user",
    }


async def test_activity_service_returns_none_when_rank_does_not_exist() -> None:
    repository = FakeActivityRepository(make_member())
    service = ActivityService(repository)  # type: ignore[arg-type]

    result = await service.get_member_rank(chat_telegram_id=-100, user_telegram_id=200)

    assert result is None
    assert repository.rank_lookup == {
        "chat_telegram_id": -100,
        "user_telegram_id": 200,
        "username": None,
    }



async def test_activity_service_returns_top_members_for_requested_chat() -> None:
    member = make_member(xp=250, level=2)
    user = make_user()
    repository = FakeActivityRepository(member)
    repository.top_result = [(member, user)]
    service = ActivityService(repository)  # type: ignore[arg-type]

    result = await service.get_top_members(chat_telegram_id=-100, limit=5)

    assert result == [(member, user)]
    assert repository.top_lookup == {"chat_telegram_id": -100, "limit": 5}


async def test_activity_service_rejects_invalid_top_limit() -> None:
    repository = FakeActivityRepository(make_member())
    service = ActivityService(repository)  # type: ignore[arg-type]

    try:
        await service.get_top_members(chat_telegram_id=-100, limit=0)
    except ValueError as error:
        assert str(error) == "limit must be between 1 and 50"
    else:
        raise AssertionError("expected ValueError for zero limit")

    assert repository.top_lookup is None
