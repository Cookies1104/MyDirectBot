# Создания таблиц БД
user_table = '''CREATE TABLE IF NOT EXISTS users 
    (id SERIAL PRIMARY KEY,
    telegram_id INTEGER NOT NULL);
'''
chapter_table = '''CREATE TABLE IF NOT EXISTS chapter
    (id SERIAL,
    user_id INTEGER REFERENCES users(id),
    chapter_name VARCHAR(200) NOT NULL PRIMARY KEY ,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
'''
element_table = '''CREATE TABLE IF NOT EXISTS element
    (element_id SERIAL,
    name VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    link TEXT,
    user_id INTEGER REFERENCES users(id),
    chapter_name VARCHAR(200) REFERENCES chapter(chapter_name),
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
'''

#--------------------------------------------
# Запросы для работы с таблицами БД
# Получаем id пользвоателя по id в телеграм
select_telegram_id = '''SELECT telegram_id FROM users'''


# Получаем элементы в разделе словаря для пользвоателя
def select_element(user_id, chapter_name):
    query = f'''SELECT name FROM element
        WHERE user_id = {user_id} AND chapter_name = {chapter_name}'''
    return query


# Обновляем название раздела для пользователя
def update_chapter(user_id, chapter_name, new_chapter_name):
    query = f'''UPDATE chapter SET chapter_name = '{new_chapter_name}'
        WHERE user_id = '{user_id}' AND 
            chapter_name = '{chapter_name}'
    '''
    return query


# Удаляем раздел для пользователя
def delete_chapter(chapter_name, telegram_user_id ):
    query = f'''
    DELETE FROM chapter USING users
        WHERE chapter.user_id = users.id
            AND chapter_name = '{chapter_name}'
            AND users.telegram_id = {telegram_user_id}
    '''
    return query


# Удаляем элемент раздела пользователя
def delete_element(chapter_name, telegram_user_id, element_name):
    query = f'''
    DELETE FROM element USING users
        WHERE element.user_id = users.id
            AND users.telegram_id = {telegram_user_id}
            AND element.chapter_name = '{chapter_name}'
            AND element.name = '{element_name}'
    '''
    return query


# Соединяем таблицы для получения списка существующих разделов у пользователя
def join_users_chapter(telegram_user_id):
    query = f'''SELECT chapter_name 
        FROM users JOIN chapter 
            ON chapter.user_id = users.id
                WHERE users.telegram_id = {telegram_user_id}'''
    return query


# Соединяем таблицы для получения списка существующих элементов для определённого раздела пользователя
def join_users_element(telegram_user_id, chapter_name):
    query = f'''SELECT name
        FROM element JOIN users
            ON element.user_id = users.id
                WHERE users.telegram_id = {telegram_user_id}
                    AND element.chapter_name = '{chapter_name}'
    '''
    return query


# Соединяем таблицы для получения описания и ссылки элемента
def join_users_element_2(telegram_user_id, chapter_name, element_name):
    query = f'''SELECT name, description, link
        FROM element JOIN users
            ON element.user_id = users.id
                WHERE users.telegram_id = {telegram_user_id}
                    AND element.chapter_name = '{chapter_name}'
                        AND element.name = '{element_name}'
    '''
    return query


# Возвращаем id пользователя
def select_user_id(telegram_user_id):
    query = f'''SELECT id FROM users WHERE telegram_id = {telegram_user_id}'''
    return query


# Создаём нового пользователя
def insert_user_telegram(telegram_user_id):
    query = f'''INSERT INTO users (telegram_id) VALUES ({telegram_user_id})'''
    return query


# Создаём новый раздел для пользователя
def insert_chapter(user_id, chapter_name):
    query = f'''INSERT INTO chapter (user_id, chapter_name) VALUES ({user_id}, '{chapter_name}')'''
    return query


# Создаём новый элемент для пользователя по разделу
def insert_element(user_id, chapter_name, element_name, element_description, element_link):
    query = f'''
        INSERT INTO element (name, description, link, user_id, chapter_name)
            VALUES ('{element_name}', '{element_description}', '{element_link}',
                    {user_id}, '{chapter_name}')'''
    return query


