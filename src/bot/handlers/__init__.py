from aiogram import Router

from bot.handlers.activity import router as activity_router
from bot.handlers.start import router as start_router

router = Router(name="handlers")
router.include_router(start_router)
router.include_router(activity_router)

__all__ = ["router"]
