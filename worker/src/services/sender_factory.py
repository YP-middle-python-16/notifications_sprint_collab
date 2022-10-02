from abc import ABC, abstractmethod
from enum import Enum


from core.config import settings
from services.email_sender import FakeEmailSender, EmailSender


class Transport(Enum):
    sms = 1
    push = 2
    email = 3


class SenderAbstract(ABC):
    @abstractmethod
    def send(self, *args, **kwargs):
        pass


class SMSSender(SenderAbstract):
    def send(self, *args, **kwargs):
        pass


class PushSender(SenderAbstract):
    def send(self, *args, **kwargs):
        pass


class InvalidSenderType(object):
    pass


class SenderFactory:
    @staticmethod
    def get_sender(transport: str) -> SenderAbstract:
        if transport == Transport.email.name:
            if settings.EMAIL_SENDER_TYPE == 'fake':
                return FakeEmailSender()
            return EmailSender()
        elif transport == Transport.sms.name:
            return SMSSender()
        elif transport == Transport.push.name:
            return PushSender()
        raise InvalidSenderType(f'Invalid sender type {transport}')
