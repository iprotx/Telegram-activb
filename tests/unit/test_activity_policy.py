from datetime import datetime, timedelta, timezone

from bot.services.activity import ActivityPolicy, level_for_xp


def test_first_message_awards_base_xp() -> None:
    policy = ActivityPolicy(base_xp=10, cooldown=timedelta(seconds=60))

    result = policy.award_xp(last_awarded_at=None, now=datetime(2026, 1, 1, tzinfo=timezone.utc))

    assert result == 10


def test_messages_inside_cooldown_award_no_xp() -> None:
    policy = ActivityPolicy(base_xp=10, cooldown=timedelta(seconds=60))
    now = datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc)

    result = policy.award_xp(last_awarded_at=now - timedelta(seconds=59), now=now)

    assert result == 0


def test_message_after_cooldown_awards_base_xp() -> None:
    policy = ActivityPolicy(base_xp=10, cooldown=timedelta(seconds=60))
    now = datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc)

    result = policy.award_xp(last_awarded_at=now - timedelta(seconds=60), now=now)

    assert result == 10


def test_level_progression_uses_quadratic_thresholds() -> None:
    assert level_for_xp(0) == 1
    assert level_for_xp(99) == 1
    assert level_for_xp(100) == 2
    assert level_for_xp(399) == 2
    assert level_for_xp(400) == 3
