import os
from typing import Final
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Config:
    BOT_TOKEN: Final = os.getenv('BOT_TOKEN', 'Впишите токен в .env!')
    ADMIN_IDS: Final = tuple(int(i) for i in str(os.getenv('BOT_ADMIN_IDS')).split(','))

    POSTBACK_PORT: Final = int(os.getenv('POSTBACK_PORT'))
    POSTBACK_BOT_TOKEN: Final = os.getenv('POSTBACK_BOT_TOKEN')
    REGISTRATION_URL = os.getenv('ONE_WIN_REGISTRATION_URL')

    @classmethod
    def get_registration_link(cls, user_id: int):
        return f"{cls.REGISTRATION_URL}&sub1={user_id}"

