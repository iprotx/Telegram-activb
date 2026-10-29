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
