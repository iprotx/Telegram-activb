from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot.handlers.welcome import welcome_new_member_handler


def make_update(
    *,
    old_status: str = "left",
    new_status: str = "member",
    is_bot: bool = False,
    chat_type: str = "supergroup",
    new_is_member: bool = True,
) -> SimpleNamespace:
    user = SimpleNamespace(is_bot=is_bot, full_name="Ada Lovelace")
    return SimpleNamespace(
        old_chat_member=SimpleNamespace(status=old_status),
        new_chat_member=SimpleNamespace(
            status=new_status,
            is_member=new_is_member,
            user=user,
        ),
        chat=SimpleNamespace(id=-100, type=chat_type),
    )


async def test_welcome_is_sent_when_a_user_joins_a_group() -> None:
    event = make_update()
    bot = SimpleNamespace(send_message=AsyncMock())

    await welcome_new_member_handler(event, bot)

    bot.send_message.assert_awaited_once_with(
        chat_id=-100,
        text="Добро пожаловать, Ada Lovelace!",
    )


async def test_welcome_is_not_sent_for_a_user_who_was_already_a_member() -> None:
    event = make_update(old_status="member", new_status="member")
    bot = SimpleNamespace(send_message=AsyncMock())

    await welcome_new_member_handler(event, bot)

    bot.send_message.assert_not_awaited()


async def test_welcome_is_not_sent_when_a_member_leaves() -> None:
    event = make_update(old_status="member", new_status="left")
    bot = SimpleNamespace(send_message=AsyncMock())

    await welcome_new_member_handler(event, bot)

    bot.send_message.assert_not_awaited()


async def test_welcome_is_not_sent_for_bots() -> None:
    event = make_update(is_bot=True)
    bot = SimpleNamespace(send_message=AsyncMock())

    await welcome_new_member_handler(event, bot)

    bot.send_message.assert_not_awaited()


async def test_welcome_is_not_sent_for_non_group_chats() -> None:
    event = make_update(chat_type="private")
    bot = SimpleNamespace(send_message=AsyncMock())

    await welcome_new_member_handler(event, bot)

    bot.send_message.assert_not_awaited()


async def test_restricted_user_is_welcomed_only_if_they_are_a_member() -> None:
    event = make_update(new_status="restricted", new_is_member=False)
    bot = SimpleNamespace(send_message=AsyncMock())

    await welcome_new_member_handler(event, bot)

    bot.send_message.assert_not_awaited()
