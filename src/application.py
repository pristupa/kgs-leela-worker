import json

import pika
import pika.amqp_object
import pika.channel

from .settings import settings
from .leela_worker import LeelaWorker


class Application:

    def __init__(self):
        parameters = pika.URLParameters(settings.amqp_url)
        self._queue = settings.amqp_queue
        self._channel = None
        self._connection = pika.SelectConnection(parameters, self._on_connected)
        self._leela_worker = LeelaWorker()

    def start(self):
        try:
            # Loop so we can communicate with RabbitMQ
            self._connection.ioloop.start()
        except KeyboardInterrupt:
            # Gracefully close the connection
            self._connection.close()
            # Loop until we're fully closed, will stop on its own
            self._connection.ioloop.start()

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
            print('[Warning] Ignoring message with invalid JSON:', body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        try:
            game_id = data['game_id']
            if not isinstance(game_id, int):
                raise ValueError()
        except (KeyError, ValueError):
            print('[Warning] Ignoring message, cannot find an integer "game_id":', body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        try:
            self._leela_worker.calculate_game(game_id)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exception:
            print('[Error]', exception)

    def _on_connected(self, connection):
        """Called when we are fully connected to RabbitMQ"""
        # Open a channel
        connection.channel(self._on_channel_open)

    def _on_channel_open(self, new_channel):
        """Called when our channel has opened"""
        self._channel = new_channel
        self._channel.queue_declare(
            queue=self._queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self._on_queue_declared,
        )

    def _on_queue_declared(self, frame):
        """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
        self._channel.basic_consume(self._handle_delivery, queue=self._queue)
