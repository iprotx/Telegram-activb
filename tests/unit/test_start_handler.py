from dataclasses import dataclass
from typing import cast

from aiogram.types import Message, User

from bot.handlers.start import start_handler
from bot.services.users import UserService


@dataclass
class FakeMessage:
    from_user: User | None
    answers: list[str]

    async def answer(self, text: str) -> None:
        self.answers.append(text)


class FakeUserService:
    def __init__(self) -> None:
        self.calls: list[tuple[int, str | None, str | None, str | None]] = []

    async def register(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        self.calls.append((telegram_id, username, first_name, last_name))
        return User(
            id=telegram_id,
            is_bot=False,
            first_name=first_name or "",
            last_name=last_name,
            username=username,
        )


async def test_start_handler_registers_telegram_profile_and_replies() -> None:
    user = User(
        id=42,
        is_bot=False,
        first_name="Alice",
        last_name="Smith",
        username="alice",
    )
    message = FakeMessage(from_user=user, answers=[])
    service = FakeUserService()

    await start_handler(cast(Message, message), cast(UserService, service))

    assert service.calls == [(42, "alice", "Alice", "Smith")]
    assert message.answers == ["Привет! Бот готов к работе."]


async def test_start_handler_preserves_missing_optional_profile_fields() -> None:
    user = User(
        id=43,
        is_bot=False,
        first_name="Bob",
        last_name=None,
        username=None,
    )
    message = FakeMessage(from_user=user, answers=[])
    service = FakeUserService()

    await start_handler(cast(Message, message), cast(UserService, service))

    assert service.calls == [(43, None, "Bob", None)]
    assert message.answers == ["Привет! Бот готов к работе."]
