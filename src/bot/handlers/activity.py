from datetime import UTC, datetime

from aiogram import F, Router
from aiogram.types import Message

from bot.services.activity_tracking import ActivityService
from bot.services.users import UserService

router = Router(name="activity")


@router.message(F.chat.type.in_({"group", "supergroup"}))
async def activity_message_handler(
    message: Message,
    user_service: UserService,
    activity_service: ActivityService,
) -> None:
    if message.from_user is None or message.message_id is None:
        return

    user = await user_service.register(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await activity_service.record_message(
        chat_telegram_id=message.chat.id,
        chat_title=message.chat.title,
        user=user,
        message_id=message.message_id,
        now=datetime.now(UTC),
    )
