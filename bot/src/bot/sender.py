import json

from aiogram import Bot

from src import log
from src.api import get_video_from_flow
from src.config import settings

from src.bot.utils import to_normal_time, delete_file


async def send_message(bot: Bot, message: str) -> None:
    """
    Send a message to channel with video or document.

    :param bot: Object of aiogram Bot
    :param message: Message in JSON format containing keyword, time range, summary, and temperature
    :return: None
    """
    message = json.loads(message)

    start_time, end_time = map(int, message["time_range"].split(" - "))

    caption = (
        f"<b>News</b>\n\n"
        f"{' - '.join(to_normal_time(float(seconds) + 60 * 60 * 3) for seconds in message['time_range'].split(' - '))}\n"
        f"<b>Summary</b>: {message['summary']}\n"
        f"<b>Temperature</b>: {message['temperature']}\n\n"
        + " ".join(f"#{tag}" for tag in message["tags"])
    )

    video = await get_video_from_flow(start_time, end_time)
    log.info(f"Video saved to {video}")

    log.info(
        f"Sending video to channel {settings.CHANNEL_NAME}, Video: {video}, Caption: {caption}"
    )
    await bot.send_video(
        chat_id=settings.CHANNEL_NAME,
        video=video,
        caption=caption,
    )

    delete_file(video)
