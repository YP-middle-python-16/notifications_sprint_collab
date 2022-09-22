import datetime
from random import randint, getrandbits

from fastapi import APIRouter

from models.models import UserInfo, MovieInfo
from . import fake

router = APIRouter()


@router.get("/auth/users",
            response_model=UserInfo,
            summary="Send user info",
            description="Send user info")
async def send_user_info(user_id: str):
    return UserInfo(
        user_id=user_id,
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        email=f'{fake.word()}@yandex.ru',
        birthday_date=(datetime.datetime.now() - datetime.timedelta(
            days=365 * randint(5, 65))).strftime('%Y-%m-%d %H:%M:%S.%f'),
    )


@router.get("/auth/movies",
            response_model=MovieInfo,
            summary="Send event to make notification",
            description="Send event to make notification")
async def send_movie_info(movie_id: str):
    return MovieInfo(
        movie_id=movie_id,
        title=' '.join([fake.word() for i in range(randint(1, 5))]),
        season=randint(0, 5) if getrandbits else None,
        episode=randint(1, 100),
        release_date=(datetime.datetime.now() + datetime.timedelta(days=randint(0, 7))).strftime('%Y-%m-%d %H:%M:%S.%f')
    )
