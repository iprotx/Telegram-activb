from dataclasses import dataclass

from bot.services.users import UserService


@dataclass
class FakeUser:
    id: int
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None


class FakeUserRepository:
    def __init__(self) -> None:
        self.calls: list[tuple[int, str | None, str | None, str | None]] = []

    async def get_or_create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> FakeUser:
        self.calls.append((telegram_id, username, first_name, last_name))
        return FakeUser(
            id=1,
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )


async def test_user_service_delegates_registration_to_repository() -> None:
    repository = FakeUserRepository()
    service = UserService(repository)

    user = await service.register(
        telegram_id=42,
        username="alice",
        first_name="Alice",
        last_name="Smith",
    )

    assert user.telegram_id == 42
    assert repository.calls == [(42, "alice", "Alice", "Smith")]
