from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from postgresql.service import ConnectDB
from postgresql.sql_query import join_users_chapter, join_users_element
from settings import function_callback, function_callback_update_element


def create_inline_button(list_button: list, row_width=5,) -> 'inline_button':
    """Возвращает инлайн кнопку"""
    inline_button = InlineKeyboardMarkup(row_width=row_width)
    for element in list_button:
        inline_button.insert(InlineKeyboardButton(element, callback_data=element))
    return inline_button


def inline_chapter(telegram_user_id) -> 'inline_button':
    """Возвращает инлайн кнопку из списка разделов пользователя.
        Список разделов загружает с БД и сортирует"""
    storage_chapter = []
    with ConnectDB() as cursor:
        # Запрос в бд на вывод всех разделов пользователя
        cursor.execute(join_users_chapter(telegram_user_id))
        for row in cursor.fetchall():
            storage_chapter.append(row[0])
    inline_kb_full = create_inline_button(sorted(storage_chapter), 3)
    return inline_kb_full


def inline_element(telegram_user_id, chapter_name) -> 'inline_button':
    """Возвращает инлайн кнопку из списка элементов раздела пользователя.
        Список элементов загружает с БД и сортирует"""
    storage_chapter = []
    with ConnectDB() as cursor:
        # Запрос в бд на вывод всех элементов пользователя
        cursor.execute(
            join_users_element(
                telegram_user_id=telegram_user_id,
                chapter_name=chapter_name
            )
        )
        for row in cursor.fetchall():
            storage_chapter.append(row[0])
    inline_kb_full = create_inline_button(sorted(storage_chapter), 3)
    return inline_kb_full


# Создаём инлайн кнопку для старта работы с ботом.
inline_kb_start = create_inline_button(function_callback, 1)

inline_update_element = create_inline_button(function_callback_update_element, 1)
