import logging
from collections.abc import Awaitable, Callable
from typing import Any, cast

import pytest
from aiogram.types import TelegramObject

from bot.middlewares.errors import ErrorMiddleware


async def test_error_middleware_logs_diagnostics_and_reraises(
    caplog: pytest.LogCaptureFixture,
) -> None:
    middleware = ErrorMiddleware()
    error = RuntimeError("database unavailable")

    async def handler(event: TelegramObject, data: dict[str, Any]) -> None:
        raise error

    with caplog.at_level(logging.ERROR, logger="bot.middlewares.errors"):
        with pytest.raises(RuntimeError) as exc_info:
            await middleware(
                cast(
                    Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                    handler,
                ),
                cast(TelegramObject, object()),
                {},
            )

    assert exc_info.value is error
    assert "Unhandled Telegram update error" in caplog.text
    assert "database unavailable" in caplog.text
    assert any(record.exc_info is not None for record in caplog.records)


async def test_error_middleware_does_not_log_update_or_context_secrets(
    caplog: pytest.LogCaptureFixture,
) -> None:
    token_sentinel = "BOT_TOKEN_SENTINEL_DO_NOT_LOG"
    payload_sentinel = '{"message":{"text":"PRIVATE_UPDATE_SENTINEL"}}'

    class SensitiveEvent:
        def __repr__(self) -> str:
            return f"update token={token_sentinel}; payload={payload_sentinel}"

    middleware = ErrorMiddleware()

    async def handler(event: TelegramObject, data: dict[str, Any]) -> None:
        raise RuntimeError("handler failed")

    with caplog.at_level(logging.ERROR, logger="bot.middlewares.errors"):
        with pytest.raises(RuntimeError, match="handler failed"):
            await middleware(
                cast(
                    Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                    handler,
                ),
                cast(TelegramObject, SensitiveEvent()),
                {
                    "bot_token": token_sentinel,
                    "serialized_update": payload_sentinel,
                },
            )

    assert "Unhandled Telegram update error" in caplog.text
    assert token_sentinel not in caplog.text
    assert payload_sentinel not in caplog.text
    assert "PRIVATE_UPDATE_SENTINEL" not in caplog.text
