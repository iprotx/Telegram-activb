from typing import Protocol

from bot.db.models import User


class UserRepositoryProtocol(Protocol):
    async def get_or_create(self, telegram_id: int, username: str | None = None) -> User: ...


class UserService:
    def __init__(self, repository: UserRepositoryProtocol) -> None:
        self._repository = repository

    async def register(self, telegram_id: int, username: str | None = None) -> User:
        return await self._repository.get_or_create(telegram_id, username)
