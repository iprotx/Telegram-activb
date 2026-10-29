import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest
from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import bot.main as main
from bot.config import Settings
from bot.db.session import Database
from bot.middlewares import ErrorMiddleware, ServicesMiddleware
from bot.routers import router


def test_import_main_has_no_runtime_side_effects(tmp_path: Path) -> None:
    environment = os.environ.copy()
    for variable in ("BOT_TOKEN", "DATABASE_URL", "LOG_LEVEL"):
        environment.pop(variable, None)

    source_path = str(Path(__file__).resolve().parents[2] / "src")
    python_path = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = os.pathsep.join(
        item for item in (source_path, python_path) if item
    )
    script = """
from unittest.mock import patch

with (
    patch("asyncio.run") as run,
    patch("aiogram.Bot") as bot,
    patch("aiogram.Dispatcher.start_polling") as polling,
    patch("bot.db.session.create_database") as create_database,
):
    import bot.main

    assert not run.called
    assert not bot.called
    assert not polling.called
    assert not create_database.called
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        check=False,
        cwd=tmp_path,
        env=environment,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr


def test_create_dispatcher_registers_middlewares_and_root_router() -> None:
    session_factory = cast(async_sessionmaker[AsyncSession], object())
    database = cast(Database, SimpleNamespace(session_factory=session_factory))

    dispatcher = main.create_dispatcher(database)

    registered_middlewares = dispatcher.update.outer_middleware._middlewares
    assert [type(middleware) for middleware in registered_middlewares] == [
        ErrorMiddleware,
        ServicesMiddleware,
    ]
    assert dispatcher.sub_routers == [router]


class FakeBotContext:
    async def __aenter__(self) -> object:
        return object()

    async def __aexit__(self, exc_type: Any, exc: Any, traceback: Any) -> bool:
        return False


async def test_run_disposes_database_when_polling_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = cast(
        Database,
        SimpleNamespace(session_factory=object(), dispose=AsyncMock()),
    )
    dispatcher = cast(
        Dispatcher,
        SimpleNamespace(
            start_polling=AsyncMock(side_effect=RuntimeError("polling failed"))
        ),
    )
    monkeypatch.setattr(main, "create_database", lambda settings: database)
    monkeypatch.setattr(
        main,
        "create_bot",
        lambda settings: cast(Bot, FakeBotContext()),
    )
    monkeypatch.setattr(main, "create_dispatcher", lambda database: dispatcher)

    with pytest.raises(RuntimeError, match="polling failed"):
        await main.run(Settings(bot_token="123:synthetic-test-token"))

    database.dispose.assert_awaited_once()
