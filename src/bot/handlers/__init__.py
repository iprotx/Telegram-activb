from aiogram import Router

from bot.handlers.activity import router as activity_router
from bot.handlers.rank import router as rank_router
from bot.handlers.start import router as start_router
from bot.handlers.top import router as top_router
from bot.handlers.welcome import router as welcome_router

router = Router(name="handlers")
router.include_router(start_router)
router.include_router(activity_router)
router.include_router(rank_router)
router.include_router(top_router)
router.include_router(welcome_router)

__all__ = ["router"]
