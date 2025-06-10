import json

from aiogram import Bot

from src.config import settings

from src.bot.utils import to_normal_time


async def send_message(bot: Bot, message: str) -> None:
    """
    Send a message to channel with video or document.

    :param bot: Object of aiogram Bot
    :param message: Message in JSON format containing keyword, time range, summary, and temperature
    :return: None
    """
    message = json.loads(message)

    caption = (
        f"<b>News</b>\n\n"
        f"{" - ".join(to_normal_time(float(seconds) + 60 * 60 * 3) for seconds in message['time_range'].split(' - '))}\n"
        f"<b>Summary</b>: {message['summary']}\n"
        f"<b>Temperature</b>: {message['temperature']}\n\n" +
        " ".join(f"#{tag}" for tag in message["tags"])
    )

    await bot.send_message(chat_id=settings.CHANNEL_NAME, text=caption)
