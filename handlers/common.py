from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from fsm import CreateElement
from buttons.inline import inline_kb_start
from postgresql.service import ConnectDB
from postgresql.sql_query import select_telegram_id, insert_user_telegram, join_users_chapter


async def send_start(msg: types.Message, state: FSMContext):
    """Функция старта в чате бота. При пользвоании ботом первый раз или отсутствия разделов в словаре у
     пользователя, возвращает запрос на создание раздела.
        При наличи разделов у пользвоателя возвращает инлайн кнопки для дальнейших действий.
        Сбрасывает состояние машины FSM в начальное.
        Переводим машину в режим ожидания действия."""
    # Сбрасываем машинное состояние
    await state.finish()

    # Создаём списки существующих пользователей и разделов для пользователя
    storage_user = []
    storage_chapter = []
    with ConnectDB() as cursor:
        cursor.execute(select_telegram_id)
        for row in cursor.fetchall():
            storage_user.append(row[0])
        cursor.execute(join_users_chapter(msg.from_user.id))
        for row in cursor.fetchall():
            storage_chapter.append(row[0])

    # Запрос в бд на создание пользователя в случае его отсутствия
    if msg.from_user.id not in storage_user:
        with ConnectDB() as cursor:
            cursor.execute(insert_user_telegram(msg.from_user.id))

    # Перевод машинного состояния в зависимости от наличия разделов у пользователя
    if len(storage_chapter) == 0:
        # Переводим машину в состояние ожидания имени раздела
        await CreateElement.waiting_for_chapter_name.set()
        await msg.answer('Для начала давайте создадим Ваш первый раздел.\n'
                         'Введите название:')
    else:
        # Переводим машину в состояние ожидания действия
        await CreateElement.waiting_for_action.set()
        await msg.answer('Выберите действие со своим словарём', reply_markup=inline_kb_start)


async def send_cancel(msg: types.Message, state: FSMContext):
    """Функция отмены любого действия в чате бота.
        Возвращает инлайн кнопки для дальнейших действий.
        Сьрасывает машинное состояние."""
    await state.finish()
    await msg.answer('Действие отменено.\n'
                     'Выберите действие со своим словарём',
                     reply_markup=inline_kb_start)


async def send_help(msg: types.Message):
    """Функция помощи. Необходимо реализовать, учитывая машинное состояние"""
    await msg.reply('Здесь должна быть помощь в пользовании ботом, но мне было лень'
                    'поэтому как-нибудь сам.')


def handlers_common(dp: Dispatcher):
    dp.register_message_handler(send_start, commands='start', state='*')
    dp.register_message_handler(send_cancel, commands=['cancel', 'отмена'], state='*')
    dp.register_message_handler(send_help, commands='help', state='*')
