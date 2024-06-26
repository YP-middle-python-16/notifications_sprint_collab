
import functools
import typing as t

import backoff
import pika

from core.config import logger

AMQP_HOSTNAME = "localhost"
AMQP_PORT = "localhost"
AMQP_USERNAME = "guest"
AMQP_PASSWORD = "guest"
AMQP_QUEUE = "low_priority"
AMQP_EXCHANGE = "low_priority"


class AmqpConnection:
    def __init__(self, hostname=AMQP_HOSTNAME, port=AMQP_PORT, username=AMQP_USERNAME, password=AMQP_PASSWORD,
                 queue=AMQP_QUEUE, exchange=AMQP_EXCHANGE):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.queue = queue
        self.exchange = exchange
        self.connection = None
        self.channel = None

    def connect(self, connection_name='Neat-App'):
        logger.info('Attempting to connect to', self.hostname)
        params = pika.ConnectionParameters(
            host=self.hostname,
            port=self.port,
            credentials=pika.PlainCredentials(self.username, self.password),
            client_properties={'connection_name': connection_name})
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()
        logger.info('Connected Successfully to', self.hostname)


    def setup_queues(self):
        self.channel.exchange_declare(self.exchange, exchange_type='direct')
        self.channel.queue_declare(self.queue)
        self.channel.queue_bind(self.queue, exchange=self.exchange, routing_key=self.queue)

    def do_async(self, callback, *args, **kwargs):
        if self.connection.is_open:
            self.connection.add_callback_threadsafe(functools.partial(callback, *args, **kwargs))

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError, max_time=60)
    def consume(self, on_message: t.Callable):
        if self.connection.is_closed or self.channel.is_closed:
            self.connect()
            self.setup_queues()
        try:
            self.channel.basic_consume(queue=self.queue, auto_ack=True, on_message_callback=on_message)
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.error('Keyboard interrupt received')
            self.channel.stop_consuming()
            self.connection.close()
            raise
        except pika.exceptions.ChannelClosedByBroker:
            logger.error('Channel Closed By Broker Exception')
            raise
