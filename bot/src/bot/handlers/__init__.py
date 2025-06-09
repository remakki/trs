from aiogram import Dispatcher

from .commands import router as commands_router


def register_handlers(dp: Dispatcher):
    dp.include_router(commands_router)
