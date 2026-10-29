from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from bot.db.models import ChatMember, User
from bot.services.activity import level_for_xp
from bot.services.activity_tracking import ActivityService

router = Router(name="rank")


@router.message(Command("rank"))
async def rank_handler(
    message: Message,
    command: CommandObject,
    activity_service: ActivityService,
) -> None:
    if message.chat.type not in {"group", "supergroup"}:
        await message.answer("Команда /rank доступна в групповых чатах.")
        return

    if message.from_user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    args = (command.args or "").split()
    if len(args) > 1 or (args and not args[0].startswith("@")):
        await message.answer("Использование: /rank или /rank @username")
        return

    if args:
        username = args[0][1:]
        if not username:
            await message.answer("Использование: /rank или /rank @username")
            return
        rank = await activity_service.get_member_rank(
            chat_telegram_id=message.chat.id,
            username=username,
        )
    else:
        rank = await activity_service.get_member_rank(
            chat_telegram_id=message.chat.id,
            user_telegram_id=message.from_user.id,
        )

    if rank is None:
        if args:
            await message.answer("У этого пользователя пока нет статистики в данном чате.")
        else:
            await message.answer("Статистика появится после первых сообщений в этом чате.")
        return

    member, user, position = rank
    await message.answer(_format_rank(member, user, position))


def _format_rank(member: ChatMember, user: User, position: int) -> str:
    level = level_for_xp(member.xp)
    current_level_xp = 100 * (level - 1) ** 2
    next_level_xp = 100 * level**2
    progress = member.xp - current_level_xp
    required = next_level_xp - current_level_xp
    display_name = f"@{user.username}" if user.username else user.first_name or "Пользователь"
    return (
        f"🏆 Статистика участника: {display_name}\n"
        f"Место в чате: #{position}\n"
        f"Уровень: {level}\n"
        f"Опыт: {member.xp} XP\n"
        f"Сообщений: {member.message_count}\n"
        f"До уровня {level + 1}: {progress}/{required} XP"
    )
