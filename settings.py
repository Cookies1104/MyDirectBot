from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, db_config

db_config = db_config
my_bot = Bot(token=TOKEN)
dispatcher = Dispatcher(my_bot, storage=MemoryStorage())

function_callback = ['Чтение',
                     'Создание записи словаря',
                     'Обновление записи в словаре',
                     'Удаление записи в словаре',
                     'Создание нового раздела',
                     'Изменение названия раздела',
                     'Удаление раздела']

function_callback_update_element = ['Название',
                                    'Описание',
                                    'Ссылку']
