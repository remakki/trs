import json

from aiogram import Bot

from src.config import settings


async def send_message(bot: Bot, message: str) -> None:
    """
    Send a message to channel with video or document.

    :param bot: Object of aiogram Bot
    :param message: Message in JSON format containing keyword, time range, summary, and temperature
    :return: None
    """
    message = json.loads(message)

    caption = (
        f"Time range: {message['time_range']}\n"
        f"Summary: {message['summary']}\n"
        f"Temperature: {message['temperature']}\n" +
        " ".join(message["tags"])
    )

    await bot.send_message(chat_id=settings.CHANNEL_NAME, text=caption)
