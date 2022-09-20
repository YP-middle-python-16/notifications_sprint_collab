import jinja2

from models.models import RawNotification

EVENT_TYPE = ['birthday', 'registration', 'reminder', 'comment_like', 'weekly_news']
TRANSPORT = ['sms', 'push', 'email']


class Templator:
    def __init__(self, notification: RawNotification):
        self.notification = notification

    def get_sms(self):
        pass

    def get_email(self):
        pass

    def get_push(self):
        pass

    def prepare(self):