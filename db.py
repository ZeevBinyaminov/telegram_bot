import json
from aiogram import types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from loader import dp

with open("users.json", "r") as users_file:
    users_dict = json.load(users_file)

with open("subjects.json", "r") as subjects_file:
    subjects_dict = json.load(subjects_file)

with open("social_media.json", "r") as social_media_file:
    social_media_dict = json.load(social_media_file)



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
