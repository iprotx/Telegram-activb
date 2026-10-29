from collections.abc import Awaitable, Callable
from typing import Any, cast

import pytest
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.middlewares.services import ServicesMiddleware
from bot.services.users import UserService


class FakeSession:
    def __init__(self) -> None:
        self.commit_calls = 0
        self.rollback_calls = 0

    async def __aenter__(self) -> "FakeSession":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, traceback: Any) -> bool:
        return False

    async def commit(self) -> None:
        self.commit_calls += 1

    async def rollback(self) -> None:
        self.rollback_calls += 1


class FakeSessionFactory:
    def __init__(self, session: FakeSession) -> None:
        self.session = session

    def __call__(self) -> FakeSession:
        return self.session


@pytest.fixture
def session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def middleware(session: FakeSession) -> ServicesMiddleware:
    factory = cast(async_sessionmaker[AsyncSession], FakeSessionFactory(session))
    return ServicesMiddleware(factory)


async def test_services_middleware_commits_after_success(
    middleware: ServicesMiddleware,
    session: FakeSession,
) -> None:
    async def handler(event: TelegramObject, data: dict[str, Any]) -> str:
        assert isinstance(data["user_service"], UserService)
        return "ok"

    result = await middleware(
        cast(Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], handler),
        cast(TelegramObject, object()),
        {},
    )

    assert result == "ok"
    assert session.commit_calls == 1
    assert session.rollback_calls == 0


async def test_services_middleware_rolls_back_and_reraises(
    middleware: ServicesMiddleware,
    session: FakeSession,
) -> None:
    error = RuntimeError("handler failed")

    async def handler(event: TelegramObject, data: dict[str, Any]) -> None:
        raise error

    with pytest.raises(RuntimeError, match="handler failed"):
        await middleware(
            cast(Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], handler),
            cast(TelegramObject, object()),
            {},
        )

    assert session.commit_calls == 0
    assert session.rollback_calls == 1
