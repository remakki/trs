import logging

from aiogram import Bot, Dispatcher

from src.bot.handlers import register_handlers
from src.bot.middlewares import BotMiddleware

logger = logging.getLogger(__name__)


async def start_bot(bot: Bot):
    dp = Dispatcher()
    dp.update.middleware(BotMiddleware(bot))
    register_handlers(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
