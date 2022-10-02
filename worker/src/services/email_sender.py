from abc import ABC, abstractmethod

from models.models import NotificationEmail


class EmailSenderAbstract(ABC):
    @abstractmethod
    def send(self, address: str, subject: str, data: str):
        pass


class FakeEmailSender(EmailSenderAbstract):
    def send(self, *args, **kwargs):
        data = args[0]
        email = NotificationEmail(**data)
        print(email)
        print('-' * 10)
        print(f'Send new email to {email.address}')
        print(f'Subject: {email.subject}')
        print(f'{email.message}')
        print('-' * 10)
        print()


class EmailSender(EmailSenderAbstract):
    def send(self, address: str, subject: str, data: str):
        pass
