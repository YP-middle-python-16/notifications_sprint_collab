from abc import ABC, abstractmethod

from core.config import settings
from services.email_sender import FakeEmailSender, EmailSender


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
        if transport == 'email':
            if settings.EMAIL_SENDER_TYPE == 'fake':
                return FakeEmailSender()
            return EmailSender()
        elif transport == 'sms':
            return SMSSender()
        elif transport == 'push':
            return PushSender()
        raise InvalidSenderType(f'Invalid sender type {transport}')
