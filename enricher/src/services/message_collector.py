from models.models import RawNotification, FinalNotification
from services.storage.base import BaseStorage
from services.transport import (
    BaseTransport,
    SMSTransport,
    EmailTransport,
    PushTransport,
)


class MessageCollector:
    def __init__(self, notification_id: str, notification: RawNotification, storage_service: BaseStorage, type: str):
        self.notification_id = notification_id
        self.notification = notification
        self.storage_service = storage_service
        self.type = type

    @staticmethod
    def get_transport_class(transport_type: str):
        return {
            'sms': SMSTransport,
            'email': EmailTransport,
            'push': PushTransport,
        }[transport_type.lower()]

    async def get_final_notifications(self) -> FinalNotification:
        transport_class = self.get_transport_class(self.notification.transport)
        transport: BaseTransport = transport_class(notification=self.notification, storage_service=self.storage_service)
        return FinalNotification(_id=self.notification_id,
                                 priority=self.notification.priority,
                                 type=self.type,
                                 transport={self.notification.transport: await transport.prepare_message()})
