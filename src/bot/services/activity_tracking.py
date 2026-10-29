from datetime import datetime
from typing import Protocol

from bot.db.models import ChatMember, User
from bot.services.activity import ActivityPolicy, level_for_xp


class ActivityRepositoryProtocol(Protocol):
    async def prepare_message(
        self,
        *,
        chat_telegram_id: int,
        chat_title: str | None,
        user: User,
        message_id: int,
    ) -> tuple[ChatMember, bool]: ...

    async def record_message(
        self,
        *,
        member: ChatMember,
        message_id: int,
        xp_awarded: int,
        new_level: int,
        now: datetime,
    ) -> ChatMember: ...

    async def get_member_rank(
        self,
        *,
        chat_telegram_id: int,
        user_telegram_id: int | None = None,
        username: str | None = None,
    ) -> tuple[ChatMember, User, int] | None: ...

    async def get_top_members(
        self,
        *,
        chat_telegram_id: int,
        limit: int = 10,
    ) -> list[tuple[ChatMember, User]]: ...


class ActivityService:
    def __init__(
        self,
        repository: ActivityRepositoryProtocol,
        policy: ActivityPolicy | None = None,
    ) -> None:
        self._repository = repository
        self._policy = policy or ActivityPolicy()

    async def record_message(
        self,
        *,
        chat_telegram_id: int,
        chat_title: str | None,
        user: User,
        message_id: int,
        now: datetime,
    ) -> ChatMember:
        member, already_recorded = await self._repository.prepare_message(
            chat_telegram_id=chat_telegram_id,
            chat_title=chat_title,
            user=user,
            message_id=message_id,
        )
        if already_recorded:
            return member

        xp_awarded = self._policy.award_xp(
            last_awarded_at=member.last_xp_at,
            now=now,
        )
        new_level = level_for_xp(member.xp + xp_awarded) if xp_awarded else member.level
        return await self._repository.record_message(
            member=member,
            message_id=message_id,
            xp_awarded=xp_awarded,
            new_level=new_level,
            now=now,
        )

    async def get_member_rank(
        self,
        *,
        chat_telegram_id: int,
        user_telegram_id: int | None = None,
        username: str | None = None,
    ) -> tuple[ChatMember, User, int] | None:
        if (user_telegram_id is None) == (username is None):
            raise ValueError("provide exactly one of user_telegram_id or username")
        return await self._repository.get_member_rank(
            chat_telegram_id=chat_telegram_id,
            user_telegram_id=user_telegram_id,
            username=username,
        )

    async def get_top_members(
        self,
        *,
        chat_telegram_id: int,
        limit: int = 10,
    ) -> list[tuple[ChatMember, User]]:
        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")
        return await self._repository.get_top_members(
            chat_telegram_id=chat_telegram_id,
            limit=limit,
        )
