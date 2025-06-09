from aiogram import Bot

from src.bot.sender import send_message
from src.config import settings
from src.mq.rabbitmq import AsyncRabbitMQ


async def start_consume(bot: Bot):
    rabbitmq = AsyncRabbitMQ()
    await rabbitmq.connect()
    await rabbitmq.consume(settings.RABBITMQ_QUEUE, callback=lambda message: send_message(bot, message))
