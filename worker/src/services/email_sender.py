from abc import ABC, abstractmethod

from core.config import logger
from models.models import NotificationEmail


class EmailSenderAbstract(ABC):
    @abstractmethod
    def send(self, address: str, subject: str, data: str):
        pass


class FakeEmailSender(EmailSenderAbstract):
    def send(self, *args, **kwargs):
        data = args[0]
        email = NotificationEmail(**data)
        logger.info(email)
        logger.info('-' * 10)
        logger.info(f'Send new email to {email.address}')
        logger.info(f'Subject: {email.subject}')
        logger.info(f'{email.message}')
        logger.info('-' * 10)


class EmailSender(EmailSenderAbstract):
    def send(self, address: str, subject: str, data: str):
        pass
