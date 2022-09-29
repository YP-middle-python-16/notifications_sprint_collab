from models.models import Email
from services.transport.base import BaseTransport


class EmailTransport(BaseTransport):
    async def prepare_message(self):
        template = await self.get_template('email')

        receivers_info_list: list[dict] = await self.get_receivers_info()
        movies_info_list: list[dict] = await self.get_movies_info()
        user_info_list: list[dict] = await self.get_users_info()

        return [Email(address=receiver['email'],
                      sender=receiver.get('sender'),
                      header=template.render(*movies_info_list,
                                             *user_info_list,
                                             **receiver),
                      message=template.render(*movies_info_list,
                                              *user_info_list,
                                              **receiver)).dict() for receiver in receivers_info_list]
