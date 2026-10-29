from dataclasses import dataclass

from bot.services.users import UserService


@dataclass
class FakeUser:
    id: int
    telegram_id: int
    username: str | None


class FakeUserRepository:
    def __init__(self) -> None:
        self.calls: list[tuple[int, str | None]] = []

    async def get_or_create(self, telegram_id: int, username: str | None = None) -> FakeUser:
        self.calls.append((telegram_id, username))
        return FakeUser(id=1, telegram_id=telegram_id, username=username)


async def test_user_service_delegates_registration_to_repository() -> None:
    repository = FakeUserRepository()
    service = UserService(repository)

    user = await service.register(telegram_id=42, username="alice")

    assert user.telegram_id == 42
    assert repository.calls == [(42, "alice")]
