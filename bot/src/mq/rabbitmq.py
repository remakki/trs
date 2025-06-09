import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from typing import Callable, Optional, Awaitable

from src.mq import logger
from src.config import settings


class AsyncRabbitMQ:
    """Асинхронный клиент для работы с RabbitMQ."""

    def __init__(self):
        """Инициализация параметров подключения к RabbitMQ."""
        self.user = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None

    async def connect(self) -> None:
        """
        Асинхронное подключение к RabbitMQ.

        Raises:
            aio_pika.exceptions.AMQPConnectionError: Если не удалось установить соединение.
        """
        try:
            logger.info(f"Подключение к RabbitMQ: {self.host}:{self.port}")
            self.connection = await aio_pika.connect_robust(
                host=self.host,
                port=self.port,
                login=self.user,
                password=self.password
            )
            self.channel = await self.connection.channel()
            logger.info("Успешное подключение к RabbitMQ")

        except aio_pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Ошибка подключения к RabbitMQ: {e}")
            raise

        except Exception as e:
            logger.error(f"Неизвестная ошибка при подключении: {e}")
            raise

    async def close(self) -> None:
        """
        Закрытие соединения с RabbitMQ.

        Raises:
            Exception: Если произошла ошибка при закрытии соединения.
        """
        try:
            if self.connection and not self.connection.is_closed:
                await self.connection.close()
                logger.info("Соединение с RabbitMQ закрыто")

        except Exception as e:
            logger.error(f"Ошибка при закрытии соединения: {e}")
            raise

    async def consume(self, queue_name: str, callback: Callable[[str], Awaitable[None]]) -> None:
        """
        Асинхронное потребление сообщений из указанной очереди.

        Args:
            queue_name: Имя очереди для потребления.
            callback: Функция обратного вызова для обработки сообщений.
                      Принимает декодированное тело сообщения (str).

        Raises:
            ValueError: Если соединение или канал не установлены.
            aio_pika.exceptions.AMQPError: Если произошла ошибка при работе с RabbitMQ.
        """
        if not self.channel:
            logger.error("Попытка потребления без установленного соединения")
            raise ValueError("Соединение не установлено")

        try:
            logger.info(f"Запуск потребления из очереди: {queue_name}")
            # Объявление очереди
            queue = await self.channel.declare_queue(queue_name, durable=True)
            # Установка ограничения на количество сообщений
            await self.channel.set_qos(prefetch_count=1)

            # Внутренний callback для обработки сообщений
            async def on_message(message: AbstractIncomingMessage):
                try:
                    async with message.process():
                        body = message.body.decode()
                        logger.info(f"Получено сообщение из очереди {queue_name}: {body}")
                        await callback(body)
                except Exception as e:
                    logger.error(f"Ошибка обработки сообщения: {e}")
                    raise

            # Запуск потребления
            await queue.consume(on_message)
            logger.info(f"Ожидание сообщений из очереди {queue_name}")

        except aio_pika.exceptions.AMQPError as e:
            logger.error(f"Ошибка при потреблении из очереди {queue_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Неизвестная ошибка при потреблении: {e}")
            raise

    async def publish(self, queue_name: str, message: str) -> None:
        """
        Асинхронная публикация сообщения в указанную очередь.

        Args:
            queue_name: Имя очереди для отправки сообщения.
            message: Сообщение для отправки (строка).

        Raises:
            ValueError: Если соединение или канал не установлены.
            aio_pika.exceptions.AMQPError: Если произошла ошибка при публикации.
        """
        if not self.channel:
            logger.error("Попытка публикации без установленного соединения")
            raise ValueError("Соединение не установлено")

        try:
            # Объявление очереди
            await self.channel.declare_queue(queue_name, durable=True)
            # Публикация сообщения
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # Сообщения сохраняются
                ),
                routing_key=queue_name
            )
            logger.info(f"Отправлено сообщение в очередь {queue_name}: {message}")
        except aio_pika.exceptions.AMQPError as e:
            logger.error(f"Ошибка при публикации в очередь {queue_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Неизвестная ошибка при публикации: {e}")
            raise