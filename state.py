from aiogram.dispatcher.filters.state import State, StatesGroup


class Subject(StatesGroup):
    subject_name = State()
    youtube_link = State()
    instagram_link = State()
    chat_link = State()
    zoom_link = State()