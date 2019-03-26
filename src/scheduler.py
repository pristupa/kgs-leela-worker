import json
from typing import Optional

import pika
import pika.amqp_object
import pika.channel

from .database import Database
from .logger import logger
from .settings import settings


class Scheduler:

    def __init__(self):
        parameters = pika.URLParameters(settings['amqp_url'])
        self._amqp_connection = pika.BlockingConnection(parameters)
        self._amqp_channel = self._amqp_connection.channel()
        self._amqp_channel.exchange_declare(exchange='kgs', exchange_type='direct', durable=True)
        self._db = Database()

    def schedule(self, n: int, kilo_playouts: Optional[int] = None):
        if kilo_playouts is None:
            kilo_playouts = int(settings['kilo_playouts'])
        try:
            logger.info(f"Adding {n} tasks (playouts={kilo_playouts}k) to the queue...")
            cursor = self._db.execute(
                "SELECT g.id FROM games g "
                "LEFT OUTER JOIN leela_results r ON r.game_id=g.id WHERE "
                "g.white_rank IN ('8d','7d','6d','5d','4d','3d','2d','1d','1k','2k','3k','4k','5k','6k','7k','8k','9k','10k') AND "
                "g.white_won IS NOT NULL AND "
                "g.black_rank IS NOT NULL AND "
                "g.handicap=0 AND "
                "g.board_size=19 AND "
                "g.timelimit>=1200 AND "
                "g.year<=2016 AND "
                "r.id IS NULL "
                "LIMIT %s",
                (n,)
            )
            for game_id, in cursor.fetchall():
                self._amqp_channel.basic_publish(
                    exchange='',
                    routing_key='kgs',
                    body=json.dumps({
                        'game_id': game_id,
                        'kilo_playouts': kilo_playouts,
                    })
                )
        except KeyboardInterrupt:
            logger.info('Gracefully closing connections...')
            self._amqp_connection.close()
