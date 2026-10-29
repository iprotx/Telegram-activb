from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.api.auth.telegram import TelegramAuthError, TelegramInitData, validate_init_data
from bot.config import Settings
from bot.db.models import Product
from bot.integrations.littlefox import LittleFoxClient, LittleFoxError
from bot.repositories.favorites import FavoriteRepository
from bot.repositories.products import ProductRepository
from bot.repositories.users import UserRepository


def create_api_app(
    settings: Settings,
    session_factory: async_sessionmaker[AsyncSession],
) -> FastAPI:
    app = FastAPI(title="KEYDROP API", version="1.0.0", docs_url="/api/docs")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    async def get_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    async def get_telegram_user(
        authorization: Annotated[str | None, Header()] = None,
    ) -> TelegramInitData:
        if not authorization or not authorization.startswith("tma "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "missing_init_data",
                    "message": "Telegram init data is required",
                },
            )

        raw_init_data = authorization[4:]
        try:
            return validate_init_data(
                raw_init_data,
                settings.bot_token_value,
                max_age_seconds=settings.telegram_init_data_max_age,
            )
        except TelegramAuthError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": exc.code, "message": str(exc)},
            ) from exc

    def get_littlefox_client() -> LittleFoxClient | None:
        if not settings.littlefox_api_key_value:
            return None
        return LittleFoxClient(settings.littlefox_base_url, settings.littlefox_api_key_value)

    async def get_customer_id(telegram: TelegramInitData, session: AsyncSession) -> int:
        user = telegram.user
        customer = await UserRepository(session).get_or_create(
            telegram_id=user.user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        return customer.id

    @app.get("/api/v1/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/v1/me")
    async def me(
        telegram: Annotated[TelegramInitData, Depends(get_telegram_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> dict[str, object | None]:
        user = telegram.user
        repository = UserRepository(session)
        customer = await repository.get_or_create(
            telegram_id=user.user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        await session.commit()

        return {
            "id": customer.id,
            "telegram_id": customer.telegram_id,
            "username": customer.username,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
        }

    @app.get("/api/v1/products")
    async def products(
        _: Annotated[TelegramInitData, Depends(get_telegram_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
        search: str | None = Query(default=None, max_length=100),
        category: str | None = Query(default=None, max_length=255),
        limit: int = Query(default=50, ge=1, le=100),
    ) -> dict[str, object]:
        client = get_littlefox_client()
        repository = ProductRepository(session)
        if client is not None:
            try:
                for item in await client.list_products(limit=limit):
                    await repository.upsert_from_provider(item)
                await session.commit()
            except LittleFoxError as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail={"code": "catalog_unavailable", "message": str(exc)},
                ) from exc

        items = await repository.list_available(search=search, category=category, limit=limit)
        return {
            "items": [serialize_product(item) for item in items],
            "limit": limit,
        }

    @app.get("/api/v1/products/{product_id}")
    async def product_detail(
        product_id: int,
        _: Annotated[TelegramInitData, Depends(get_telegram_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> dict[str, object | None]:
        product = await ProductRepository(session).get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "not_found", "message": "Product not found"},
            )
        return serialize_product(product)

    @app.get("/api/v1/favorites")
    async def favorites(
        telegram: Annotated[TelegramInitData, Depends(get_telegram_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> dict[str, list[int]]:
        customer_id = await get_customer_id(telegram, session)
        return {"product_ids": await FavoriteRepository(session).list_product_ids(customer_id)}

    @app.put("/api/v1/favorites/{product_id}")
    async def add_favorite(
        product_id: int,
        telegram: Annotated[TelegramInitData, Depends(get_telegram_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> dict[str, bool]:
        customer_id = await get_customer_id(telegram, session)
        try:
            await FavoriteRepository(session).add(customer_id, product_id)
        except LookupError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "not_found", "message": "Product not found"},
            ) from exc
        await session.commit()
        return {"favorite": True}

    @app.delete("/api/v1/favorites/{product_id}")
    async def remove_favorite(
        product_id: int,
        telegram: Annotated[TelegramInitData, Depends(get_telegram_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> dict[str, bool]:
        customer_id = await get_customer_id(telegram, session)
        await FavoriteRepository(session).remove(customer_id, product_id)
        await session.commit()
        return {"favorite": False}

    return app


def serialize_product(product: Product) -> dict[str, object | None]:
    return {
        "id": product.id,
        "provider_product_id": product.provider_product_id,
        "name": product.name,
        "description": product.description,
        "description_html": product.description_html,
        "price_kopeks": product.price_kopeks,
        "currency": product.currency,
        "stock": product.stock,
        "stock_unlimited": product.stock_unlimited,
        "available": product.available,
        "category": product.category,
    }
