import json
import logging
from config import ADMIN_ID

from aiogram.types import Message, CallbackQuery
from loader import dp

from keyboards.inline.choice_buttons import main_menu, social_media_menu, subjects_menu
from keyboards.inline.callback_data import subject_choice_callback, social_media_choice_callback

from db import subjects_dict, social_media_dict


@dp.message_handler(commands=["start", "items"])
async def welcome(message: Message):
    command = message.get_command()
    command_text = {
        '/start': "Привет!\n"
                  "Я - бот-навигатор, помогаю найти необходимые ссылки и чаты.\n"
                  "Что тебя интересует ?",
        '/items': 'Что тебя интересует ?',

    }

    # ---- Добавление нового пользователя в словарь и учет кликов
    with open("users.json", "r") as users_file:
        users_dict = json.load(users_file)
    print(users_dict)
    user_id = str(message.from_user.id)
    username = message.from_user.username

    if user_id not in users_dict:
        users_dict[user_id] = {
            "username": username,
            "visits": 0
        }
    users_dict[user_id]["visits"] += 1

    with open("users.json", "w") as users_file:
        json.dump(users_dict, users_file, indent=4, ensure_ascii=False)
    # ----

    await message.answer(
        text=command_text[command],
        reply_markup=main_menu
    )


@dp.callback_query_handler(text='social media')
async def choose_social_media(call: CallbackQuery):
    await call.answer(cache_time=2)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer(text='Наши соцсети:', reply_markup=social_media_menu)


@dp.callback_query_handler(text='subjects')
async def choose_subjects(call: CallbackQuery):
    await call.answer(cache_time=2)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer(text='Выбери предмет:', reply_markup=subjects_menu)


@dp.callback_query_handler(text='back')
async def back(call: CallbackQuery):
    await call.answer(cache_time=2)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer(text='Что тебя интересует ?', reply_markup=main_menu)


@dp.callback_query_handler(subject_choice_callback.filter())
async def choose_subject(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    logging.info(f"call = {callback_data}")
    subject = callback_data.get('subject_name')
    await call.message.answer(text=subjects_dict[subject])


@dp.callback_query_handler(social_media_choice_callback.filter())
async def choose_social_media(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    logging.info(f"call = {callback_data}")
    social_media = callback_data.get('social_media_name')
    social_media_dict[social_media]["clicks"] += 1
    await call.message.answer(
        text=f"Ссылка на {social_media}: \n"
             f"{social_media_dict[social_media]['url']}"
    )


@dp.message_handler(commands=["add_subject"], user_id=ADMIN_ID)
async def add_subject(message: Message):
    await message.answer("Введи название предмета")
