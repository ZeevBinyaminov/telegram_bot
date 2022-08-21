import json
from aiogram import types
from loader import dp

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

with open("users.json", "r") as users_file:
    users_dict = json.load(users_file)

with open("subjects.json", "r") as subjects_file:
    subjects_dict = json.load(subjects_file)

with open("social_media.json", "r") as social_media_file:
    social_media_dict = json.load(social_media_file)
