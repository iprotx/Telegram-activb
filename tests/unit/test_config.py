import pytest
from pydantic import ValidationError

from bot.config import Settings, get_database_url


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


def test_settings_reject_database_url_without_async_driver(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/bot")

    with pytest.raises(ValidationError, match="async database driver"):
        Settings()


def test_settings_accept_postgresql_asyncpg(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://localhost/bot")

    settings = Settings()

    assert settings.database_url == "postgresql+asyncpg://localhost/bot"


def test_get_database_url_loads_dotenv(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    (tmp_path / ".env").write_text(
        "DATABASE_URL=sqlite+aiosqlite:///./from-env-file.db\n",
        encoding="utf-8",
    )

    assert get_database_url() == "sqlite+aiosqlite:///./from-env-file.db"


def test_get_database_url_prefers_environment_over_dotenv(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "DATABASE_URL=sqlite+aiosqlite:///./from-env-file.db\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./from-environment.db")

    assert get_database_url() == "sqlite+aiosqlite:///./from-environment.db"


@pytest.mark.parametrize(
    "log_level",
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
)
def test_settings_accept_standard_log_levels(
    monkeypatch: pytest.MonkeyPatch,
    log_level: str,
) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("LOG_LEVEL", log_level)

    settings = Settings()

    assert settings.log_level == log_level


def test_settings_reject_unknown_log_level(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:test")
    monkeypatch.setenv("LOG_LEVEL", "TRACE")

    with pytest.raises(ValidationError, match="log level"):
        Settings()
