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


def make_init_data(bot_token: str) -> str:
    values = {
        "auth_date": str(int(datetime.now(UTC).timestamp())),
        "user": '{"id":123456789,"first_name":"Test"}',
    }
    check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), sha256).digest()
    digest = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()
    return urlencode({**values, "hash": digest})


@pytest.mark.asyncio
async def test_products_returns_server_stored_catalog() -> None:
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
                    description="Description",
                    description_html="<strong>Description</strong>",
                    price_kopeks=19900,
                    currency="RUB",
                    stock=5,
                    stock_unlimited=False,
                    available=True,
                    category="Subscriptions",
                )
            )
            await session.commit()

        settings = Settings(bot_token="123456:TEST")
        app = create_api_app(settings, session_factory)
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/products",
                headers={"Authorization": f"tma {make_init_data(settings.bot_token_value)}"},
            )

        assert response.status_code == 200
        assert response.json()["items"][0]["name"] == "Test product"
        assert response.json()["items"][0]["price_kopeks"] == 19900
    finally:
        await engine.dispose()
