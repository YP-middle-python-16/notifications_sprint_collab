import typing as t
from abc import abstractmethod

import aiohttp
from jinja2 import Template
from jinja2.nativetypes import NativeEnvironment

from core.config import settings
from models.models import RawNotification
from services.storage.base import BaseStorage


class BaseTransport:
    def __init__(self, notification: RawNotification, storage_service: BaseStorage):
        self.notification = notification
        self.template_name = notification.payload.template
        self._template_env = None
        self.storage_service = storage_service

    async def get_template(self, transport_type: str) -> Template:
        """
        Чтение шаблона jinja из хранилища
        :param transport_type: [sms, push, email]
        """
        template_list = await self.storage_service.select({'name': self.template_name,
                                                           'transport': transport_type}, settings.MONGO_TEMPLATE_TABLE)
        template = template_list.pop()
        env = NativeEnvironment()
        return env.from_string(template['body'])

    @abstractmethod
    async def prepare_message(self, *args, **kwargs):
        raise NotImplementedError('method is not implemented!')

    @staticmethod
    async def _get_info(endpoint: str, obj_id: str) -> dict:
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            url = (f'http://{settings.FAKE_GENERATOR_API_HOST.rstrip("/")}:'
                   f'{settings.FAKE_GENERATOR_API_PORT}/'
                   f'{endpoint.lstrip("/")}={obj_id}')
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    async def _get_user_info(self, user_id: str):
        """
        Получение информации о пользователе по его айди
        :param user_id: айди
        """
        return await self._get_info(settings.USER_INFO_ENDPOINT, user_id)

    async def _get_movie_info(self, movie_id: str):
        """
        Получение информации о фильме по его айди
        :param movie_id: айди
        """
        return await self._get_info(settings.USER_INFO_ENDPOINT, movie_id)

    async def get_receivers_info(self) -> t.Generator:
        """
        Получение информации о всех получателях, указанных в событии
        """
        receivers_list = self.notification.receivers_list
        for receiver_id in receivers_list:
            yield self._get_user_info(receiver_id)

    async def get_users_info(self) -> t.Generator:
        """
        Получение информации о всех пользователях, указанных в событии
        """
        user_id_list = self.notification.payload.body.get('user_ids')
        for user_id in user_id_list:
            yield self._get_user_info(user_id)

    async def get_movies_info(self) -> t.Generator:
        """
        Получение информации о всех фильмах, указанных в событии
        """
        movie_ids: t.Union[list] = self.notification.payload.body.get('movie_ids', [])
        for movie_id in movie_ids:
            yield self._get_movie_info(movie_id)
