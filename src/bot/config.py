from logging import getLevelNamesMapping

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


_ASYNC_DATABASE_DRIVERS = {
    "sqlite+aiosqlite",
    "postgresql+asyncpg",
    "postgresql+psycopg",
    "mysql+aiomysql",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: SecretStr
    database_url: str = "sqlite+aiosqlite:///./bot.db"
    log_level: str = "INFO"

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        try:
            url = make_url(value)
        except Exception as exc:
            raise ValueError("DATABASE_URL must be a valid SQLAlchemy URL") from exc

        if url.drivername not in _ASYNC_DATABASE_DRIVERS:
            raise ValueError("DATABASE_URL must use a supported async SQLAlchemy driver")

        return value

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in getLevelNamesMapping():
            raise ValueError("LOG_LEVEL must be a valid Python logging level")
        return normalized

    @property
    def bot_token_value(self) -> str:
        return self.bot_token.get_secret_value()
