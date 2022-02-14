from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateElement(StatesGroup):
    """Машинное состояние для создания элемента словаря"""
    waiting_for_action = State()
    waiting_for_chapter_name = State()
    waiting_for_update_chapter_name = State()
    waiting_for_element_name = State()
    waiting_for_element_description = State()
    waiting_for_element_link = State()
    element_name_read = State()
    element_name_update = State()
    element_update = State()
    element_name_delete = State()
