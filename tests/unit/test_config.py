import logging

import pytest
from pydantic import ValidationError

from bot.config import Settings


def test_settings_load_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

    settings = Settings()

    assert settings.bot_token_value == "123:test"
    assert settings.database_url == "sqlite+aiosqlite:///./test.db"


def test_settings_require_bot_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    with pytest.raises(ValidationError):
        Settings()


def test_settings_reject_invalid_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("DATABASE_URL", "not-a-database-url")

    with pytest.raises(ValidationError, match="DATABASE_URL"):
        Settings()


def test_settings_reject_unsupported_database_driver(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/bot")

    with pytest.raises(ValidationError, match="DATABASE_URL"):
        Settings()


def test_settings_validate_log_level(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("LOG_LEVEL", "not-a-level")

    with pytest.raises(ValidationError, match="LOG_LEVEL"):
        Settings()

    for level in logging.getLevelNamesMapping():
        if isinstance(logging.getLevelNamesMapping()[level], int):
            monkeypatch.setenv("LOG_LEVEL", level)
            assert Settings().log_level == level
