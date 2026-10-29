from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
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
        if last_awarded_at is None or now - last_awarded_at >= self.cooldown:
            return self.base_xp
        return 0


def level_for_xp(xp: int) -> int:
    if xp < 0:
        raise ValueError("xp must not be negative")
    return isqrt(xp // 100) + 1
