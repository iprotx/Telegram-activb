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


def make_member(
    *, xp: int = 0, level: int = 1, last_xp_at: datetime | None = None
) -> ChatMember:
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
