from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot.db.models import ChatMember, User
from bot.handlers.rank import _format_rank, rank_handler


def make_member(*, xp: int = 250, level: int = 2, message_count: int = 12) -> ChatMember:
    return ChatMember(
        id=1,
        chat_id=10,
        user_id=20,
        xp=xp,
        level=level,
        message_count=message_count,
        last_xp_at=None,
    )


def make_user(*, username: str | None = "test-user") -> User:
    return User(
        id=20,
        telegram_id=200,
        username=username,
        first_name="Test",
        last_name=None,
    )


def make_message(*, chat_type: str = "supergroup") -> SimpleNamespace:
    return SimpleNamespace(
        chat=SimpleNamespace(type=chat_type, id=-100),
        from_user=SimpleNamespace(id=200),
        answer=AsyncMock(),
    )


async def test_rank_handler_shows_self_stats_and_level_progress() -> None:
    message = make_message()
    service = SimpleNamespace(
        get_member_rank=AsyncMock(return_value=(make_member(), make_user(), 2))
    )

    await rank_handler(message, SimpleNamespace(args=None), service)

    service.get_member_rank.assert_awaited_once_with(
        chat_telegram_id=-100,
        user_telegram_id=200,
    )
    message.answer.assert_awaited_once_with(
        "🏆 Статистика участника: @test-user\n"
        "Место в чате: #2\n"
        "Уровень: 2\n"
        "Опыт: 250 XP\n"
        "Сообщений: 12\n"
        "До уровня 3: 150/300 XP"
    )


async def test_rank_handler_can_look_up_username_in_current_chat() -> None:
    message = make_message()
    service = SimpleNamespace(get_member_rank=AsyncMock(return_value=None))

    await rank_handler(message, SimpleNamespace(args="@other-user"), service)

    service.get_member_rank.assert_awaited_once_with(
        chat_telegram_id=-100,
        username="other-user",
    )
    message.answer.assert_awaited_once_with(
        "У этого пользователя пока нет статистики в данном чате."
    )


async def test_rank_handler_rejects_invalid_arguments() -> None:
    message = make_message()
    service = SimpleNamespace(get_member_rank=AsyncMock())

    await rank_handler(message, SimpleNamespace(args="not-a-username"), service)

    service.get_member_rank.assert_not_awaited()
    message.answer.assert_awaited_once_with("Использование: /rank или /rank @username")


async def test_rank_handler_explains_private_chat_limitation() -> None:
    message = make_message(chat_type="private")
    service = SimpleNamespace(get_member_rank=AsyncMock())

    await rank_handler(message, SimpleNamespace(args=None), service)

    service.get_member_rank.assert_not_awaited()
    message.answer.assert_awaited_once_with("Команда /rank доступна в групповых чатах.")


def test_rank_progress_uses_current_level_threshold() -> None:
    text = _format_rank(make_member(xp=400, level=3), make_user(username=None), 1)

    assert "Уровень: 3" in text
    assert "До уровня 4: 0/500 XP" in text
