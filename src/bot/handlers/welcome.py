from aiogram import Bot, Router
from aiogram.types import ChatMemberUpdated

router = Router(name="welcome")


@router.chat_member()
async def welcome_new_member_handler(event: ChatMemberUpdated, bot: Bot) -> None:
    if event.chat.type not in {"group", "supergroup"}:
        return

    new_member = event.new_chat_member
    if new_member.user.is_bot:
        return

    old_member = event.old_chat_member
    was_member = _is_active_member(
        old_member.status,
        is_member=getattr(old_member, "is_member", False),
    )
    is_member = _is_active_member(
        new_member.status,
        is_member=getattr(new_member, "is_member", False),
    )
    if was_member or not is_member:
        return

    await bot.send_message(
        chat_id=event.chat.id,
        text=f"Добро пожаловать, {new_member.user.full_name}!",
    )


def _is_active_member(status: str, *, is_member: bool = False) -> bool:
    return status in {"creator", "administrator", "member"} or (
        status == "restricted" and is_member
    )
