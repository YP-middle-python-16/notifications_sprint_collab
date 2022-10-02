import argparse
import json
import typing as t

import requests
from pydantic import ValidationError

from amqpconnection import AmqpConnection
from core.config import settings, logger
from models.models import EnrichedNotification
from services.sender_factory import SenderFactory


"""
Пример сообщения в брокере
message = {
    "notification_id": "str",
    "priority": "hight",
    "type": "transactional",
    "transport": {
        "email": {
            "address": "apenshin@gmail.com",
            "message": "1",
            "subject": "Тестовое письмо"
        }
        
    }
}
"""



def decode_data_from_json(data: str) -> t.Union[None, t.Dict]:
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return None



def on_message(channel, method, properties, body) -> None:
    body = decode_data_from_json(body)
    if type(body) is not dict:
        logger.error('Error send message. Empty or not json')
        return
    try:
        msg = EnrichedNotification(**body)
    except ValidationError as e:
        raise ValueError('Error message')

    for transport in msg.transport:
        sender = SenderFactory.get_sender(transport)
        response = sender.send(msg.transport.get(transport))
        try:
            r = requests.post(
                f"http://{settings.NOTIFICATION_HOST.rstrip('/')}:{settings.NOTIFICATION_PORT}/"
                f"{settings.SEND_EVENT_ENDPOINT.lstrip('/')}/{msg.notification_id}",
                params={"status": "250"})
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


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
