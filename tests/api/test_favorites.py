from datetime import UTC, datetime
import hmac
from hashlib import sha256
from urllib.parse import urlencode

import httpx
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.api.app import create_api_app
from bot.config import Settings
from bot.db.base import Base
from bot.db.models import Product, User  # noqa: F401


def make_init_data(bot_token: str, user_id: int) -> str:
    values = {
        "auth_date": str(int(datetime.now(UTC).timestamp())),
        "user": f'{{"id":{user_id},"first_name":"Test"}}',
    }
    check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), sha256).digest()
    digest = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()
    return urlencode({**values, "hash": digest})


@pytest.mark.asyncio
async def test_favorites_are_scoped_to_authenticated_customer() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        async with session_factory() as session:
            session.add(
                Product(
                    provider_product_id=42,
                    name="Test product",
                    price_kopeks=100,
                    currency="RUB",
                    stock=None,
                    stock_unlimited=True,
                    available=True,
                )
            )
            await session.commit()

        settings = Settings(bot_token="123456:TEST")
        app = create_api_app(settings, session_factory)
        transport = httpx.ASGITransport(app=app)
        headers_a = {"Authorization": f"tma {make_init_data(settings.bot_token_value, 1)}"}
        headers_b = {"Authorization": f"tma {make_init_data(settings.bot_token_value, 2)}"}

        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            added = await client.put("/api/v1/favorites/1", headers=headers_a)
            favorites_a = await client.get("/api/v1/favorites", headers=headers_a)
            favorites_b = await client.get("/api/v1/favorites", headers=headers_b)

        assert added.status_code == 200
        assert favorites_a.json()["product_ids"] == [1]
        assert favorites_b.json()["product_ids"] == []
    finally:
        await engine.dispose()
