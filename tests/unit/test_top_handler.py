from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot.db.models import ChatMember, User
from bot.handlers.top import top_handler


def make_member(*, xp: int, level: int, message_count: int) -> ChatMember:
    return ChatMember(
        id=xp,
        chat_id=10,
        user_id=xp,
        xp=xp,
        level=level,
        message_count=message_count,
        last_xp_at=None,
    )


def make_user(username: str) -> User:
    return User(
        id=1,
        telegram_id=200,
        username=username,
        first_name=username.title(),
        last_name=None,
    )


def make_message(*, chat_type: str = "supergroup") -> SimpleNamespace:
    return SimpleNamespace(
        chat=SimpleNamespace(type=chat_type, id=-100),
        answer=AsyncMock(),
    )


async def test_top_handler_renders_top_ten_for_current_chat() -> None:
    message = make_message()
    top_members = [
        (make_member(xp=300, level=2, message_count=5), make_user("second-user")),
        (make_member(xp=200, level=2, message_count=4), make_user("third-user")),
    ]
    service = SimpleNamespace(get_top_members=AsyncMock(return_value=top_members))

    await top_handler(message, service)

    service.get_top_members.assert_awaited_once_with(chat_telegram_id=-100, limit=10)
    message.answer.assert_awaited_once_with(
        "🏆 Топ участников чата:\n"
        "1. @second-user — 300 XP, ур. 2, сообщений: 5\n"
        "2. @third-user — 200 XP, ур. 2, сообщений: 4"
    )


async def test_top_handler_reports_empty_chat() -> None:
    message = make_message()
    service = SimpleNamespace(get_top_members=AsyncMock(return_value=[]))

    await top_handler(message, service)

    message.answer.assert_awaited_once_with("Пока нет статистики активности в этом чате.")


async def test_top_handler_is_only_available_in_group_chats() -> None:
    message = make_message(chat_type="private")
    service = SimpleNamespace(get_top_members=AsyncMock())

    await top_handler(message, service)

    service.get_top_members.assert_not_awaited()
    message.answer.assert_awaited_once_with("Команда /top доступна в групповых чатах.")
