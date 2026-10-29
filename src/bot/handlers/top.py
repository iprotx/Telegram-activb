from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db.models import ChatMember, User
from bot.services.activity import level_for_xp
from bot.services.activity_tracking import ActivityService

router = Router(name="top")


@router.message(Command("top"))
async def top_handler(message: Message, activity_service: ActivityService) -> None:
    if message.chat.type not in {"group", "supergroup"}:
        await message.answer("Команда /top доступна в групповых чатах.")
        return

    top_members = await activity_service.get_top_members(chat_telegram_id=message.chat.id, limit=10)
    if not top_members:
        await message.answer("Пока нет статистики активности в этом чате.")
        return

    lines = ["🏆 Топ участников чата:"]
    for position, (member, user) in enumerate(top_members, start=1):
        lines.append(_format_top_entry(position, member, user))
    await message.answer("\n".join(lines))


def _format_top_entry(position: int, member: ChatMember, user: User) -> str:
    display_name = f"@{user.username}" if user.username else user.first_name or "Пользователь"
    level = level_for_xp(member.xp)
    return (
        f"{position}. {display_name} — {member.xp} XP, "
        f"ур. {level}, сообщений: {member.message_count}"
    )
