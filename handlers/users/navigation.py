import json
import logging
from config import ADMIN_ID

from aiogram.types import Message, CallbackQuery
from loader import dp

from keyboards.inline.choice_buttons import main_menu, social_media_menu, subjects_menu
from keyboards.inline.callback_data import subject_choice_callback, social_media_choice_callback

from aiogram.dispatcher import FSMContext
from state import Subject

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


@dp.message_handler(commands=["add_subject"], user_id=ADMIN_ID, state=None)
async def add_subject(message: Message):
    await Subject.subject_name.set()
    await message.answer("Введи название предмета")


@dp.message_handler(user_id=ADMIN_ID, state=Subject.subject_name)
async def add_subject_name(message: Message, state: FSMContext):
    if message.text in subjects_dict:
        await message.answer(text="Такой предмет уже есть!")
        await state.reset_state()
    else:
        async with state.proxy() as data:
            data['subject_name'] = message.text

        await Subject.next()
        await message.answer("Теперь введи ссылку на youtube-плейлист")


@dp.message_handler(user_id=ADMIN_ID, state=Subject.youtube_link)
async def add_youtube_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['youtube_link'] = message.text

    await Subject.next()
    await message.answer("Теперь введи ссылку на instagram-плейлист")


@dp.message_handler(user_id=ADMIN_ID, state=Subject.instagram_link)
async def add_instagram_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['instagram_link'] = message.text

    await Subject.next()
    await message.answer("Теперь введи ссылку на чат")


@dp.message_handler(user_id=ADMIN_ID, state=Subject.chat_link)
async def add_instagram_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat_link'] = message.text

    await Subject.next()
    await message.answer("И, наконец, введи ссылку на zoom")


@dp.message_handler(user_id=ADMIN_ID, state=Subject.zoom_link)
async def add_instagram_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['zoom_link'] = message.text

    await add_subject_json(state)
    print(subjects_dict)
    await state.finish()

    await message.answer(text=f"Предмет \"{data['subject_name']}\" успешно добавлен")


async def add_subject_json(state: FSMContext):
    async with state.proxy() as data:
        keys = list(data.keys())
        subjects_dict[data[keys[0]]] = {keys[i]: data[keys[i]] for i in range(1, 5)}

    with open("subjects.json", "w") as subjects_file:
        json.dump(subjects_dict, subjects_file, indent=4, ensure_ascii=False)
