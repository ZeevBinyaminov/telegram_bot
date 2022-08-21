from json import load
from aiogram import types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command

from loader import dp

# subjects_dict = load(open("subjects.json"))

subjects_dict = {
    "Матан": {
        "Youtube": 'https://youtube.com',
        "Instagram": '',
        "Чат во Вконтакте": '',
        "Ссылка на зум": '',
    },
    "Линал": {
        "Youtube": 'https://youtube.com',
        "Instagram": '',
        "Чат во Вконтакте": '',
        "Ссылка на зум": '',
    },
}

social_media_dict = {
    'Вконтакте': {
        "clicks": 0,
        "url": 'https://vk.com/optimum_iq',
    },

    'Telegram': {
        "clicks": 0,
        "url": 'https://t.me/optimumclub',
    },
    'Instagram': {
        "clicks": 0,
        "url": 'https://t.me/optimumclub',
    },
}


class Subject(StatesGroup):
    subject_name = State()
    chat_link = State()
    youtube_link = State()
    zoom_link = State()


@dp.message_handler(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None

    await state.reset_state()



