from datetime import UTC, datetime
from hashlib import sha256
import hmac
from urllib.parse import urlencode

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.api.app import create_api_app
from bot.config import Settings
from bot.db.base import Base
from bot.db.models import User  # noqa: F401


def make_init_data(bot_token: str, *, user_id: int = 123456789) -> str:
    values = {
        "auth_date": str(int(datetime.now(UTC).timestamp())),
        "user": f'{{"id":{user_id},"first_name":"Test","username":"tester"}}',
    }
    check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), sha256).digest()
    digest = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()
    return urlencode({**values, "hash": digest})


def test_me_creates_customer_from_valid_telegram_init_data() -> None:
    async def setup():
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        return engine

    import asyncio

    engine = asyncio.run(setup())
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    settings = Settings(bot_token="123456:TEST")
    app = create_api_app(settings, session_factory)

    with TestClient(app) as client:
        response = client.get(
            "/api/v1/me",
            headers={"Authorization": f"tma {make_init_data(settings.bot_token_value)}"},
        )

    assert response.status_code == 200
    assert response.json()["telegram_id"] == 123456789
    assert response.json()["username"] == "tester"

    asyncio.run(engine.dispose())
