from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from fsm import CreateElement
from settings import my_bot
from buttons.inline import function_callback, inline_chapter, inline_kb_start, inline_element, \
    inline_update_element
from postgresql.service import ConnectDB, select_query, use_database
from postgresql.sql_query import select_user_id, join_users_chapter, insert_chapter, delete_chapter, update_chapter, \
    insert_element, join_users_element_2, delete_element


async def callback_button_action(callback_query: types.CallbackQuery, state: FSMContext):
    """Возвращает список разделов пользователя в виде инлайн кнопок.
        Если выбран пункт создания раздела - ожидает ввод навзания нового раздела.
        Записывает действие в машинное состояние."""
    # Обновляем данные в состоянии машины
    await state.update_data(action=callback_query.data)
    # переводим машину в режим ожидания названия раздела
    await CreateElement.waiting_for_chapter_name.set()

    # Возвращаем инлайн кнопки в зависимости от выбранного действия
    # Возвращаем инлайн кнопку в видел элементов раздела пользователя для чтения
    if callback_query.data == function_callback[0]:
        await my_bot.send_message(callback_query.from_user.id,
                                  'Выберите раздел для чтения элементов словаря',
                                  reply_markup=inline_chapter(callback_query.from_user.id))
    # Возвращаем инлайн кнопку в виде разделов пользователя для создания записи в конкретном разделе
    elif callback_query.data == function_callback[1]:
        await my_bot.send_message(callback_query.from_user.id,
                                  'Выберите раздел для создания элементов словаря',
                                  reply_markup=inline_chapter(callback_query.from_user.id))
    # Возвращаем инлайн кнопку в виде разделов пользователя для обновления существующих элементов в конкретном разделе
    elif callback_query.data == function_callback[2]:
        await my_bot.send_message(callback_query.from_user.id,
                                  'Выберите раздел для обновления элементов словаря',
                                  reply_markup=inline_chapter(callback_query.from_user.id))
    # Возвращаем инлайн кнопку в виде разделов пользователя для удаления существующих элементов в конкретном разделе
    elif callback_query.data == function_callback[3]:
        await my_bot.send_message(callback_query.from_user.id,
                                  'Выберите раздел для удаления элементов словаря',
                                  reply_markup=inline_chapter(callback_query.from_user.id))
    # Запрашиваем название нового раздела
    elif callback_query.data == function_callback[4]:
        await CreateElement.waiting_for_chapter_name.set()
        await my_bot.send_message(callback_query.from_user.id,
                                  'Введите название нового раздела:')
    # Возвращаем инлайн кнопку из разделов пользователя для изменения названия раздела
    elif callback_query.data == function_callback[5]:
        await my_bot.send_message(callback_query.from_user.id,
                                  'Выберите раздел для изменение названия',
                                  reply_markup=inline_chapter(callback_query.from_user.id))
    # Возвращаем инлайн кнопку из разделов пользователя для удаления всего раздела
    elif callback_query.data == function_callback[6]:
        await my_bot.send_message(callback_query.from_user.id,
                                  'Выберите раздел для удаления',
                                  reply_markup=inline_chapter(callback_query.from_user.id))


async def callback_other(callback_query: types.CallbackQuery, state: FSMContext):
    """Принимает запрос от инлайн кнопки с названием раздела.
        Возвращает сообщение с описанием дальнейших действий"""
    # Получаем данные из состояния машины
    data = await state.get_data()
    # Переводим в начало работы с ботом, если сбросилось состояние машины.
    if data['action'] is None:
        await my_bot.send_message(
            callback_query.from_user.id,
            'Вы не запутались? Вот я запутался. Давайте начнём с начала',
            reply_markup=inline_kb_start
        )
        await CreateElement.waiting_for_action.set()
    else:
        # Обновляем данные в состоянии машины
        await state.update_data(chapter_name=callback_query.data)

        # Создаём инлайн кнопку элементов пользователя для конкретного раздела
        elements = inline_element(callback_query.from_user.id, callback_query.data)

        # Возвращаем элементы раздела в виде инлайн кнопки, в случае отсутствия элементов предлагает создание нового
        # Запрашиваем название для чтения
        if data['action'] == function_callback[0]:
            if len(elements['inline_keyboard']) == 0:
                await my_bot.send_message(
                    callback_query.from_user.id,
                    'У вас пока нет элементов в данном разделе.\n'
                    'Введите название нового элемента:'
                )
                await CreateElement.waiting_for_element_name.set()
            else:
                await my_bot.send_message(
                    callback_query.from_user.id,
                    f'Выберите элемент чтения для раздела - {callback_query.data}',
                    reply_markup=elements
                )
                await CreateElement.element_name_read.set()
        # Запрашиваем название нового элемента
        elif data['action'] == function_callback[1]:
            await my_bot.send_message(callback_query.from_user.id,
                                      f'Введите название элемента для создания в разделе '
                                      f'- {callback_query.data}')
            await CreateElement.waiting_for_element_name.set()
        # Обновление записи в словаре
        elif data['action'] == function_callback[2]:
            if len(elements['inline_keyboard']) == 0:
                await my_bot.send_message(
                    callback_query.from_user.id,
                    'У вас пока нет элементов в данном разделе.\n'
                    'Введите название нового элемента:'
                )
                await CreateElement.waiting_for_element_name.set()
            else:
                await my_bot.send_message(callback_query.from_user.id,
                                          'Выберите элемент который хотите изменить',
                                          reply_markup=elements
                                          )
                await CreateElement.element_name_update.set()
        # Удаление записи в словаре
        elif data['action'] == function_callback[3]:
            if len(elements['inline_keyboard']) == 0:
                await my_bot.send_message(
                    callback_query.from_user.id,
                    'У вас пока нет элементов в данном разделе.\n'
                    'Введите название нового элемента:'
                )
                await CreateElement.waiting_for_element_name.set()
            else:
                await my_bot.send_message(callback_query.from_user.id,
                                          f'Введите элемент для удаления'
                                          f'- {callback_query.data}',
                                          reply_markup=elements)
                await CreateElement.element_name_delete.set()
        # Создание нового раздела
        elif data['action'] == function_callback[4]:
            await CreateElement.waiting_for_chapter_name.set()
        # Изменение названия раздела
        elif data['action'] == function_callback[5]:
            await my_bot.send_message(callback_query.from_user.id,
                                      f'Введите новое название для раздела "{callback_query.data}"')
            await CreateElement.waiting_for_update_chapter_name.set()
        # Удаление раздела
        elif data['action'] == function_callback[6]:
            use_database(
                delete_chapter(
                    chapter_name=callback_query.data,
                    telegram_user_id=callback_query.from_user.id
                )
            )
            await my_bot.send_message(callback_query.from_user.id,
                                      f'Раздел "{callback_query.data}" успешно удалён')


async def callback_read_element(callback_query: types.CallbackQuery, state: FSMContext):
    """Принимает запрос от инлайн кнопки с названием элемента и возвращает описание, ссылку"""
    # Обновляем данные в машине состояния
    await state.update_data(element_name=callback_query.data)

    # Получаем данные из состояния машины
    data = await state.get_data()

    # Получаем данные об элементе из БД
    with ConnectDB() as cursor:
        cursor.execute(join_users_element_2(callback_query.from_user.id,
                                            data['chapter_name'],
                                            data['element_name']))
        storage = cursor.fetchall()[0]

    # Возвращаем описание и ссылку элемента пользователю
    await my_bot.send_message(
        callback_query.from_user.id,
        f'{callback_query.data} - {storage[1]}.\n Ссылка на ресурс для подробностей:\n{storage[2]}',
    )

    # Сбрасываем состояние машины
    await state.finish()


async def handler_create_element_chapter(msg: types.Message, state: FSMContext):
    """Принимает название элемента в разделе и запрашивает ввести описание элемента"""
    # Создаём список разделов пользователя
    storage_chapter = []
    with ConnectDB() as cursor:
        cursor.execute(join_users_chapter(msg.from_user.id))
        for row in cursor.fetchall():
            storage_chapter.append(row[0])

    # Проверяем название
    if msg.text.lower() in storage_chapter:
        await msg.answer('Такой элемент уже существует, воспользуйтесь функцией обновления '
                         'или введите другое название')
        return

    # Обновляем данные в машине состояния
    await state.update_data(element_name=msg.text.lower())

    # Переводим машину в состояния ожидания описания элемента
    await CreateElement.waiting_for_element_description.set()
    await msg.reply(f'Введите описание элемента {msg.text.lower()}')


async def handler_create_element_description(msg: types.Message, state: FSMContext):
    """Принимает описание элемента и запрашивает ввести ссылку на ресурс элемента"""
    # Обновляем данные в машине состояния
    await state.update_data(element_description=msg.text)

    # Переводим машину в состояния ожидания ссылки на ресурс элемента
    await CreateElement.waiting_for_element_link.set()
    user_data = await state.get_data()
    await msg.reply(f'Добавьте ссылку на ресурс для подробного писания элемента {user_data["element_name"]}')


async def handler_create_element_link(msg: types.Message, state: FSMContext):
    """Принимает ссылку элемента и сохранает все данные об элементе в БД"""
    # Получаем данные из состояния машины
    data = await state.get_data()
    print(state)

    # Получаем id пользователя в БД
    with ConnectDB() as cursor:
        cursor.execute(select_user_id(msg.from_user.id))
        user_id = cursor.fetchone()[0]

    # Сохраняем элемент в БД
    use_database(
        insert_element(
            user_id=user_id,
            chapter_name=data['chapter_name'],
            element_name=data['element_name'],
            element_description=data['element_description'],
            element_link=msg.text
        )
    )

    # Сбрасываем состояние машины
    await state.finish()
    await msg.reply(f'Сохранение элемента {data["element_name"]} успешно выполнено!', reply_markup=inline_kb_start)


async def callback_update_element(callback_query: types.CallbackQuery, state: FSMContext):
    """Принимает запрос от инлайн кнопки с названием элемента,
    возвращает инлайн кнопку с выбором действия"""
    await state.update_data(element_name=callback_query.data)
    await my_bot.send_message(callback_query.from_user.id,
                              'Выберите что именно хотите изменить',
                              reply_markup=inline_update_element)
    await CreateElement.element_update.set()


# async def callback_update_element_2(callback_query: types.CallbackQuery, state: FSMContext):
#     """Принимает запрос от инлайн кнопки с выбранным действием для редактирования элемента,
#     предлагает ввести новые параметры"""
#     da


async def callback_del_element(callback_query: types.CallbackQuery, state: FSMContext):
    """Принимает запрос от инлайн кнопки с названием элемента и удаляет его"""
    # Получаем данные из состояния машины
    data = await state.get_data()

    # Делаем запрос в БД для удаления элемента
    use_database(
        delete_element(
            chapter_name=data['chapter_name'],
            telegram_user_id=callback_query.from_user.id,
            element_name=callback_query.data
        )
    )

    # Сбрасываем состояние машины
    await my_bot.send_message(callback_query.from_user.id,
                              f'Элемент с названием "{callback_query.data}" успешно удалён')
    await state.finish()


async def handler_update_chapter_name(msg: types.Message, state: FSMContext):
    """Проверяет новое название раздела на наличие в БД. В случае отсутствия изменяет название раздела.
        В случае наличия, запрашивает ввести другое название."""
    # Создаём спсиок разделов пользователя, а также получаем id пользователя в БД
    storage_chapter = []
    with ConnectDB() as cursor:
        cursor.execute(join_users_chapter(msg.from_user.id))
        for row in cursor.fetchall():
            storage_chapter.append(row[0])
        cursor.execute(select_user_id(msg.from_user.id))
        user_id = cursor.fetchone()[0]

    # Проверяем новое название
    if msg.text.lower() in storage_chapter:
        await msg.answer('Такое название раздела уже существует, введите другое название')
        return

    # Создаём запрос на изменение названия раздела
    data = await state.get_data()
    use_database(update_chapter(
        user_id=user_id,
        chapter_name=data['chapter_name'],
        new_chapter_name=msg.text)
    )
    await msg.answer(f'Название раздела "{data["chapter_name"]}" успешно изменено на "{msg.text}"')
    await state.finish()


async def handler_create_chapter(msg: types.Message, state: FSMContext):
    """Принимает запрос на создание нового раздела. Выполняет проверку на наличие раздела
       с таким же именем в БД.
           Запрашивает название элемента раздела.
           Переводит машинное состояние в режим ожидания имени элемента раздела."""
    # Создаём список разделов пользователя
    storage_chapter = []
    with ConnectDB() as cursor:
        cursor.execute(join_users_chapter(msg.from_user.id))
        for row in cursor.fetchall():
            storage_chapter.append(row[0])

    # Проверяем название
    if msg.text.lower() in storage_chapter:
        await msg.answer('Такое название раздела уже существует, введите другое название')
        return

    # Обновляем данные в машине состояния
    await state.update_data(chapter_name=msg.text.lower())

    # Получаем id пользователя в БД, а также создаём новый раздел
    with ConnectDB() as cursor:
        cursor.execute(select_user_id(msg.from_user.id))
        user_id = cursor.fetchone()[0]
        cursor.execute(insert_chapter(user_id, msg.text.lower()))

    # Переводим машину в состояния ожидания имени элемента
    await msg.answer(f'Раздел с навзанием "{msg.text.title()}" успешно создан.\n'
                     f'Теперь давайте создадим новый элемент.\n'
                     f'Введите название элемента:')
    await CreateElement.waiting_for_element_name.set()


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(callback_button_action,
                                       lambda c: c.data in function_callback,
                                       state='*')
    dp.register_message_handler(handler_create_chapter, state=CreateElement.waiting_for_chapter_name)
    dp.register_callback_query_handler(callback_other,
                                       lambda c: c.data in select_query(
                                           join_users_chapter(
                                               c.from_user.id
                                           )
                                       ),
                                        state='*')
    dp.register_message_handler(handler_update_chapter_name, state=CreateElement.waiting_for_update_chapter_name)
    dp.register_message_handler(handler_create_element_chapter, state=CreateElement.waiting_for_element_name)
    dp.register_message_handler(handler_create_element_description, state=CreateElement.waiting_for_element_description)
    dp.register_message_handler(handler_create_element_link, state=CreateElement.waiting_for_element_link)
    dp.register_callback_query_handler(callback_read_element, state=CreateElement.element_name_read)
    dp.register_callback_query_handler(callback_del_element, state=CreateElement.element_name_delete)
    dp.register_callback_query_handler(callback_update_element, state=CreateElement.element_name_update)
