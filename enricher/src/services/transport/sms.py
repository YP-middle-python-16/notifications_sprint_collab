from models.models import SMS
from services.transport.base import BaseTransport


class SMSTransport(BaseTransport):
    async def prepare_message(self):
        template = await self.get_template('sms')

        receivers_info_list: list[dict] = await self.get_receivers_info()
        movies_info_list: list[dict] = await self.get_movies_info()
        user_info_list: list[dict] = await self.get_users_info()

        return [SMS(address=receiver['telephone_number'],
                    message=template.render(*movies_info_list,
                                            *user_info_list,
                                            **receiver)).dict() for receiver in receivers_info_list]
