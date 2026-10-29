from aiogram import Router

from bot.handlers import router as handlers_router

router = Router(name="root")
router.include_router(handlers_router)
