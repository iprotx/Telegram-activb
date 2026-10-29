from datetime import datetime

from bot.db.models import ChatMember, User
from bot.repositories.activity import ActivityRepository


class ActivityService:
    def __init__(self, repository: ActivityRepository) -> None:
        self._repository = repository

    async def record_message(
        self,
        *,
        chat_telegram_id: int,
        chat_title: str | None,
        user: User,
        message_id: int,
        now: datetime,
    ) -> ChatMember:
        return await self._repository.record_message(
            chat_telegram_id=chat_telegram_id,
            chat_title=chat_title,
            user=user,
            message_id=message_id,
            now=now,
        )
