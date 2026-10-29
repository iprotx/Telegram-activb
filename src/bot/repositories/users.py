from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_or_create(self, telegram_id: int, username: str | None = None) -> User:
        result = await self._session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user is not None:
            return user

        user = User(telegram_id=telegram_id, username=username)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
