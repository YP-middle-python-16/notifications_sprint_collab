import argparse
import json
import logging

import requests
from amqpconnection import AmqpConnection

import time

from models.models import EnrichedNotification
from core.config import settings
from pydantic import ValidationError

from services.sender_factory import SenderFactory

logger = logging.getLogger(__name__)

message = {
    "_id": "str",
    "notification_id": "str",
    "priority": "hight",
    "type": "transactional",
    "transport": {
        "email": {
            "address": "apenshin@gmail.com",
            "message": "1",
            "subject": "Тестовое письмо"
        },
        "sms": {
            "number": "+71231231212",
            "message": "str"
        },
        "push": {
            "device": "",
            "message": "str"
        }
    }
}


def decode_data_from_json(data):
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return None


def on_message(channel, method, properties, body):
    body = decode_data_from_json(body)
    if not body:
        logger.error('Error send message. Empty or not json')
        return
    try:
        msg = EnrichedNotification(**body)
    except ValidationError as e:
        raise ValueError('Error message')
    print(msg)
    id = "633155227c4b6f5fb5bb8cf5"
    for transport in msg.transport:
        sender = SenderFactory.get_sender(transport)
        response = sender.send(msg.transport.get(transport))
        r = requests.post(f"http://localhost:8000/api/v1/event/status/{id}", json={"status": "250"})
        print(r.text)



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--priority", action='store_true', help="priority queue, default false")
    parser.set_defaults(priority=False)

    args = parser.parse_args()
    if args.priority:
        queue_settings = settings.rabbit_hight_priority
    else:
        queue_settings = settings.rabbit_low_priority

    mq = AmqpConnection(hostname=settings.RABBIT_HOST, port=settings.RABBIT_PORT,
                        username=settings.RABBIT_USER, password=settings.RABBIT_PASSWORD,
                        queue=queue_settings.queue, exchange=queue_settings.exchange)
    mq.connect()
    mq.setup_queues()

    mq.consume(on_message)


if __name__ == '__main__':
    main()
