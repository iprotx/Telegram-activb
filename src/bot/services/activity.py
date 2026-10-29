from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from math import isqrt


@dataclass(frozen=True, slots=True)
class ActivityPolicy:
    base_xp: int = 10
    cooldown: timedelta = timedelta(seconds=60)

    def __post_init__(self) -> None:
        if self.base_xp <= 0:
            raise ValueError("base_xp must be positive")
        if self.cooldown.total_seconds() < 0:
            raise ValueError("cooldown must not be negative")

    def award_xp(self, *, last_awarded_at: datetime | None, now: datetime) -> int:
        if last_awarded_at is None:
            return self.base_xp

        last_awarded_utc = _as_utc(last_awarded_at)
        now_utc = _as_utc(now)
        if now_utc - last_awarded_utc >= self.cooldown:
            return self.base_xp
        return 0


def _as_utc(value: datetime) -> datetime:
    """Normalize timestamps to UTC; naive database timestamps are interpreted as UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def level_for_xp(xp: int) -> int:
    if xp < 0:
        raise ValueError("xp must not be negative")
    return isqrt(xp // 100) + 1
