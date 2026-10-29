from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_or_create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        result = await self._session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user is not None:
            self._synchronize_profile(user, username, first_name, last_name)
            return user

        try:
            async with self._session.begin_nested():
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                self._session.add(user)
                await self._session.flush()
        except IntegrityError:
            result = await self._session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one()
            self._synchronize_profile(user, username, first_name, last_name)
            return user

        await self._session.refresh(user)
        return user

    @staticmethod
    def _synchronize_profile(
        user: User,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
    ) -> None:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
