import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from handlers.callback import register_callback
from handlers.common import handlers_common
from settings import dispatcher, my_bot

from postgresql.service import use_database
from postgresql.sql_query import user_table, chapter_table, element_table

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/cancel', description='Отменить текущее действие'),
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/help', description='Запуск помощи в работе с ботом')
    ]
    await bot.set_my_commands(commands)


async def main():
    # logging.basicConfig(level=logging.INFO,
    #                     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    #                     )
    # logger.error("Starting bot")

    handlers_common(dispatcher)
    register_callback(dispatcher)

    await set_commands(bot=my_bot)

    await dispatcher.start_polling()


# Создание таблиц в БД
use_database(user_table)
use_database(chapter_table)
use_database(element_table)


if __name__ == '__main__':
    # executor.start_polling(dp)
    asyncio.run(main())

