from aiogram import executor
from aiogram.types import BotCommand

from src.filters import register_all_filters
from src.handlers import register_all_handlers
from src.database import register_models
from src.create_bot import dp, bot
from src.utils import logger


async def on_startup(_):
    # await bot.set_my_commands(commands=[BotCommand('/game', 'Change game')])

    # Регистрация фильтров
    register_all_filters(dp)

    # Регистрация хэндлеров
    register_all_handlers(dp)

    # Регистрация моделей базы данных
    register_models()

    logger.info('Бот запущен!')


async def on_shutdown(_):
    await (await bot.get_session()).close()


def start_bot():
    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    except Exception as e:
        logger.error(e)
