from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import ActivityEvent, Chat, ChatMember, User


class ActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def prepare_message(
        self,
        *,
        chat_telegram_id: int,
        chat_title: str | None,
        user: User,
        message_id: int,
    ) -> tuple[ChatMember, bool]:
        chat = await self._get_or_create_chat(chat_telegram_id, chat_title)
        member = await self._get_or_create_member(chat.id, user.id)

        event = await self._session.execute(
            select(ActivityEvent).where(
                ActivityEvent.chat_member_id == member.id,
                ActivityEvent.telegram_message_id == message_id,
            )
        )
        return member, event.scalar_one_or_none() is not None

    async def record_message(
        self,
        *,
        member: ChatMember,
        message_id: int,
        xp_awarded: int,
        new_level: int,
        now: datetime,
    ) -> ChatMember:
        member.message_count += 1
        member.xp += xp_awarded
        member.level = new_level
        if xp_awarded:
            member.last_xp_at = now

        self._session.add(
            ActivityEvent(
                chat_member_id=member.id,
                telegram_message_id=message_id,
                xp_awarded=xp_awarded,
            )
        )
        await self._session.flush()
        return member

    async def _get_or_create_chat(self, telegram_id: int, title: str | None) -> Chat:
        result = await self._session.execute(select(Chat).where(Chat.telegram_id == telegram_id))
        chat = result.scalar_one_or_none()
        if chat is not None:
            chat.title = title
            return chat

        try:
            async with self._session.begin_nested():
                chat = Chat(telegram_id=telegram_id, title=title)
                self._session.add(chat)
                await self._session.flush()
        except IntegrityError:
            pass

        result = await self._session.execute(select(Chat).where(Chat.telegram_id == telegram_id))
        return result.scalar_one()

    async def _get_or_create_member(self, chat_id: int, user_id: int) -> ChatMember:
        result = await self._session.execute(
            select(ChatMember)
            .where(ChatMember.chat_id == chat_id, ChatMember.user_id == user_id)
            .with_for_update()
        )
        member = result.scalar_one_or_none()
        if member is not None:
            return member

        try:
            async with self._session.begin_nested():
                member = ChatMember(chat_id=chat_id, user_id=user_id)
                self._session.add(member)
                await self._session.flush()
        except IntegrityError:
            pass

        # Lock the row after a concurrent insert wins the unique-key race. Without this,
        # concurrent first messages can both update the same member without serialization.
        result = await self._session.execute(
            select(ChatMember).where(
                ChatMember.chat_id == chat_id, ChatMember.user_id == user_id
            )
            .with_for_update()
        )
        return result.scalar_one()
