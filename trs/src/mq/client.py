from __future__ import annotations

from typing import Optional

import pika
from pika import BlockingConnection
from pika.channel import Channel
from pika.exceptions import AMQPConnectionError

from src.config import settings


class RabbitMQ:
    """
    RabbitMQ client for publishing messages to a specified queue.
    """

    def __init__(self):
        self.user = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.connection: Optional[BlockingConnection] = None
        self.channel: Optional[Channel] = None

    def connect(self) -> None:
        """
        Establish a connection to the RabbitMQ server.
        :return: None
        """
        if not all([self.host, self.port, self.user, self.password]):
            raise ValueError("")

        try:
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=credentials
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
        except AMQPConnectionError as e:
            raise
        except Exception as e:
            raise

    def close(self) -> None:
        """
        Close the connection to the RabbitMQ server.
        """
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except Exception as e:
            raise

    def __enter__(self) -> RabbitMQ:
        """
        Context manager entry point for RabbitMQ connection.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Context manager exit point for RabbitMQ connection.
        """
        self.close()

    def publish(self, queue_name: str, message: str) -> None:
        """
        Publish a message to the specified RabbitMQ queue.
        :param queue_name: The name of the queue to publish the message to.
        :param message: The message to be published.
        :return: None
        """
        if not self.channel:
            raise ValueError("")

        try:
            # Объявление очереди
            self.channel.queue_declare(queue=queue_name, durable=True)
            # Публикация сообщения
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Сообщения сохраняются
                ),
            )
        except pika.exceptions.AMQPError as e:
            raise
        except Exception as e:
            raise
