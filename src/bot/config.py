import logging

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./bot.db"

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        url = make_url(value)
        if url.drivername not in {"sqlite+aiosqlite", "postgresql+asyncpg"}:
            raise ValueError("database_url must use an async database driver")
        return value


class Settings(DatabaseSettings):
    bot_token: SecretStr
    log_level: str = "INFO"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    telegram_init_data_max_age: int = 3600
    cors_origins: list[str] = ["http://localhost:5173"]
    littlefox_api_key: SecretStr | None = None
    littlefox_base_url: str = "https://littlefox-api.ru/api/v1"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in logging.getLevelNamesMapping():
            raise ValueError("log_level must be a standard Python log level")
        return normalized

    @field_validator("telegram_init_data_max_age")
    @classmethod
    def validate_init_data_max_age(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("telegram_init_data_max_age must be positive")
        return value

    @property
    def bot_token_value(self) -> str:
        return self.bot_token.get_secret_value()

    @property
    def littlefox_api_key_value(self) -> str | None:
        return self.littlefox_api_key.get_secret_value() if self.littlefox_api_key else None


def get_database_url() -> str:
    return DatabaseSettings().database_url
