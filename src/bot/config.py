from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: SecretStr
    database_url: str = "sqlite+aiosqlite:///./bot.db"
    log_level: str = "INFO"

    @property
    def bot_token_value(self) -> str:
        return self.bot_token.get_secret_value()
