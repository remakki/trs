import asyncio
import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot import start_bot
from src.config import settings
from src.mq.consume import start_consume


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    os.makedirs("data", exist_ok=True)
    await asyncio.gather(start_bot(bot), start_consume(bot))


if __name__ == "__main__":
    asyncio.run(main())
