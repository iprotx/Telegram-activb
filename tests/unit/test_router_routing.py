import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

ROUTING_SCRIPT = r"""
import asyncio
import json
import sys
from unittest.mock import AsyncMock, patch

from aiogram import Bot, Dispatcher
from aiogram.types import Message, User

from bot.handlers import router


class FakeUserService:
    def __init__(self):
        self.register_calls = 0

    async def register(self, **kwargs):
        self.register_calls += 1
        return object()


class FakeActivityService:
    def __init__(self):
        self.record_calls = 0
        self.rank_calls = 0
        self.top_calls = 0

    async def record_message(self, **kwargs):
        self.record_calls += 1

    async def get_member_rank(self, **kwargs):
        self.rank_calls += 1
        return None

    async def get_top_members(self, **kwargs):
        self.top_calls += 1
        return []


async def main():
    content = json.loads(sys.argv[1])
    update = {
        "update_id": 1,
        "message": {
            "message_id": 10,
            "date": 1_798_761_600,
            "chat": {"id": -100123, "type": "supergroup", "title": "Test group"},
            "from": {
                "id": 200,
                "is_bot": False,
                "first_name": "Test",
                "username": "test-user",
            },
            **content,
        },
    }
    user_service = FakeUserService()
    activity_service = FakeActivityService()

    async with Bot(token="123456:synthetic-test-token") as bot:
        bot._me = User(
            id=123456,
            is_bot=True,
            first_name="Routing test bot",
            username="Resagaibot",
        )
        dispatcher = Dispatcher()
        dispatcher.include_router(router)
        with patch.object(Message, "answer", new_callable=AsyncMock) as answer:
            await dispatcher.feed_raw_update(
                bot,
                update,
                user_service=user_service,
                activity_service=activity_service,
            )

    print(
        json.dumps(
            {
                "answer": answer.await_count,
                "register": user_service.register_calls,
                "record": activity_service.record_calls,
                "rank": activity_service.rank_calls,
                "top": activity_service.top_calls,
            }
        )
    )


asyncio.run(main())
"""

PHOTO = {
    "photo": [
        {
            "file_id": "synthetic-photo",
            "file_unique_id": "synthetic-photo-unique",
            "width": 1,
            "height": 1,
            "file_size": 1,
        }
    ]
}


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        pytest.param(
            {"text": "/top"},
            {"answer": 1, "register": 0, "record": 0, "rank": 0, "top": 1},
            id="top",
        ),
        pytest.param(
            {"text": "/top@Resagaibot"},
            {"answer": 1, "register": 0, "record": 0, "rank": 0, "top": 1},
            id="top-addressed-to-this-bot",
        ),
        pytest.param(
            {"text": "/rank"},
            {"answer": 1, "register": 0, "record": 0, "rank": 1, "top": 0},
            id="rank",
        ),
        pytest.param(
            {"text": "/rank@Resagaibot"},
            {"answer": 1, "register": 0, "record": 0, "rank": 1, "top": 0},
            id="rank-addressed-to-this-bot",
        ),
        pytest.param(
            {"text": "/top@AnotherBot"},
            {"answer": 0, "register": 0, "record": 0, "rank": 0, "top": 0},
            id="command-addressed-to-another-bot",
        ),
        pytest.param(
            {"text": "/unknown"},
            {"answer": 0, "register": 0, "record": 0, "rank": 0, "top": 0},
            id="unknown-command",
        ),
        pytest.param(
            {**PHOTO, "caption": "/unknown"},
            {"answer": 0, "register": 0, "record": 0, "rank": 0, "top": 0},
            id="unknown-caption-command",
        ),
        pytest.param(
            {"text": "ordinary message"},
            {"answer": 0, "register": 1, "record": 1, "rank": 0, "top": 0},
            id="ordinary-message",
        ),
        pytest.param(
            PHOTO,
            {"answer": 0, "register": 1, "record": 1, "rank": 0, "top": 0},
            id="non-text-message",
        ),
    ],
)
def test_handlers_router_routes_commands_before_activity(
    content: dict[str, Any],
    expected: dict[str, int],
    tmp_path: Path,
) -> None:
    environment = os.environ.copy()
    source_path = str(Path(__file__).resolve().parents[2] / "src")
    python_path = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = os.pathsep.join(item for item in (source_path, python_path) if item)

    result = subprocess.run(
        [sys.executable, "-c", ROUTING_SCRIPT, json.dumps(content)],
        capture_output=True,
        check=False,
        cwd=tmp_path,
        env=environment,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == expected
