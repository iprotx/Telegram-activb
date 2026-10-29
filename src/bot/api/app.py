from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.api.auth.telegram import TelegramAuthError, TelegramInitData, validate_init_data
from bot.config import Settings
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
        allow_methods=["GET"],
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

    return app
