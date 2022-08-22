from aiogram.dispatcher.filters.state import State, StatesGroup


class Subject(StatesGroup):
    subject_name = State()
    youtube_link = State()
    instagram_link = State()
    chat_link = State()
    zoom_link = State()


class Event(StatesGroup):
    event_name = State()
    event_text = State()
    event_date = State()
    event_time = State()
