import jinja2
from jinja2.nativetypes import NativeEnvironment

from core.config import settings
from models.models import (
    RawNotification,
    SMS,
    Push,
    Email,
    ORJSONModel,
)


class Templator:
    def __init__(self, notification: RawNotification, context: dict):
        self.notification = notification
        self.template_name = notification.payload.template
        self.context = context  # тут уже обогащенная информация
        self._template_env = None

    @property
    def template_env(self):
        if not self._template_env:
            template_loader = jinja2.FileSystemLoader(searchpath=settings.TEMPLATE_PATH)
            self._template_env = jinja2.Environment(loader=template_loader)

        return self._template_env

    def get_template(self, transport_type: str):
        template_filename = f'{self.template_name}_{transport_type}.html'
        return self.template_env.get_template(template_filename)

    def get_sms(self) -> SMS:
        template = self.get_template('sms')
        message = template.render(**self.context)

        return SMS(number=self.context.get('number'),
                   message=message)

    def get_email(self) -> Email:
        template = self.get_template('email')
        env = NativeEnvironment()
        t = env.from_string(self.notification.payload.header)
        header = t.render(**self.context)
        message = template.render(**self.context)

        return Email(address=self.context.get('email'),
                     sender=self.context.get('sender'),
                     header=header,
                     message=message)

    def get_push(self) -> Push:
        template = self.get_template('push')
        message = template.render(**self.context)

        return Push(device=self.context.get('email'),
                    message=message)

    def _get_for_transport(self, transport: str) -> ORJSONModel:
        return {
            'sms': self.get_sms(),
            'email': self.get_email(),
            'push': self.get_push()
        }.get(transport)

    def get_prepared_notification_for_transport(self) -> dict:
        result_dict = dict()
        for transport_type in self.notification.transport:
            result_dict[transport_type] = self._get_for_transport(transport_type)

        return result_dict
