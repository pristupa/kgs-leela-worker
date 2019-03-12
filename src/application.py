import json
import time

import pika
import pika.amqp_object
import pika.channel

from .database import Database
from .leela_worker import GameNotFoundError
from .leela_worker import LeelaWorker
from .logger import logger
from .settings import settings


class Application:

    def __init__(self):
        parameters = pika.URLParameters(settings.amqp_url)
        self._amqp_channel = None
        self._amqp_connection = pika.SelectConnection(parameters, self._on_connected)
        self._database = Database()
        self._leela_worker = LeelaWorker(self._database.connection)

    def start(self):
        try:
            logger.info(f'Working with {settings.playouts} playouts')
            time.sleep(3)
            logger.info('Listening the queue...')
            # Loop so we can communicate with RabbitMQ
            self._amqp_connection.ioloop.start()
        except KeyboardInterrupt:
            logger.info('Gracefully closing connections...')
            try:
                # Gracefully close the connections
                self._database.close()
                self._amqp_connection.close()
                # Loop until we're fully closed, will stop on its own
                self._amqp_connection.ioloop.start()
            except Exception:
                pass  # Fail silently

    def _handle_delivery(
            self,
            channel: pika.channel.Channel,
            method: pika.spec.Basic.Deliver,
            properties: pika.BasicProperties,
            body: bytes,
    ):
        """Called when we receive a message from RabbitMQ"""
        try:
            data = json.loads(body)
        except json.decoder.JSONDecodeError:
            logger.warn(f'Ignoring message with invalid JSON: {body}')
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        try:
            game_id = data['game_id']
            if not isinstance(game_id, int):
                raise ValueError(f'Invalid game_id: {game_id}')
        except (KeyError, ValueError):
            logger.warn(f'Ignoring message, cannot find an integer "game_id": {body}')
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        try:
            self._leela_worker.calculate_game(game_id)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except GameNotFoundError:
            logger.error(f'Ignoring message, game not found: {game_id}')
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

    def _on_connected(self, connection):
        """Called when we are fully connected to RabbitMQ"""
        # Open a channel
        connection.channel(self._on_channel_open)

    def _on_channel_open(self, new_channel):
        """Called when our channel has opened"""
        self._amqp_channel = new_channel
        self._amqp_channel.queue_declare(
            queue=settings.amqp_queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self._on_queue_declared,
        )

    def _on_queue_declared(self, frame):
        """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
        self._amqp_channel.basic_consume(self._handle_delivery, queue=settings.amqp_queue)
