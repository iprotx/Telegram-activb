from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.services.users import UserService

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: Message, user_service: UserService) -> None:
    if message.from_user is None:
        return

    await user_service.register(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
    )
    await message.answer("Привет! Бот готов к работе.")
