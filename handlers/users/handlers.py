import asyncio
import json
import logging
from datetime import datetime, timedelta
from config import OPTIMUM_CHAT_ID

from loader import dp, bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from keyboards.inline.choice_buttons import main_menu, social_media_menu, subjects_menu, events_menu, \
    make_events_menu, make_subjects_menu
from keyboards.inline.callback_data import subject_choice_callback, social_media_choice_callback, event_choice_callback

from aiogram.dispatcher import FSMContext
from state import Subject, Event

from db import subjects_dict, social_media_dict, events_dict


@dp.message_handler(commands=["start", "menu"])
async def welcome(message: Message):
    command = message.get_command()
    command_text = {
        '/start': "Привет!\n"
                  "Я - бот-навигатор по Оптимуму.\n\n"
                  "🤓У нас проходят занятия по основным предметам"
                  " (нажимай «предметы» и сможешь найти ссылки на записи занятий и на образовательные видео)\n\n"
                  "🚀Ещё мы проводим разные мероприятия, чтобы узнать про ближайшее, нажимай «события»\n\n"
                  "Также здесь вы можете найти ссылки на наши социальные сети, "
                  "чтобы оставаться на связи и читать наши полезные посты на любимой платформе💜",

        '/menu': 'Что тебя интересует ?',

    }

    # ---- Добавление нового пользователя в словарь и учет кликов
    with open("users.json", "r") as users_file:
        users_dict = json.load(users_file)
        user_id = str(message.from_user.id)
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

    if user_id not in users_dict:
        users_dict[user_id] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }

    with open("users.json", "w") as users_file:
        json.dump(users_dict, users_file, indent=4, ensure_ascii=False)
    # ----

    await message.answer(
        text=command_text[command],
        reply_markup=main_menu
    )


@dp.callback_query_handler(text='social media')
async def choose_social_media(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.edit_text(text='Наши соцсети:')
    await call.message.edit_reply_markup(reply_markup=social_media_menu)


@dp.message_handler(commands=['social_media'])
async def get_social_media(message: Message):
    await message.answer(text='Наши соцсети:', reply_markup=social_media_menu)


@dp.callback_query_handler(text='subjects')
async def choose_subjects(call: CallbackQuery):
    await call.answer(cache_time=2)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.edit_text(text='Выбери предмет:')
    await call.message.edit_reply_markup(reply_markup=subjects_menu)


@dp.message_handler(commands=['subjects'])
async def get_subjects(message: Message):
    await message.answer(text='Предметы: ', reply_markup=subjects_menu)


@dp.callback_query_handler(text="events")
async def choose_events(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    if events_menu == InlineKeyboardMarkup():
        await call.message.edit_text(text="На ближайшее вреня нет событийю\n"
                                          "Нажмите на /menu, чтобы вернуться в начало")
    else:
        await call.message.edit_text(text="Список ближайших событий")
        await call.message.edit_reply_markup(reply_markup=events_menu)


@dp.message_handler(commands=['events'])
async def get_events(message: Message):
    if events_menu == InlineKeyboardMarkup():
        await message.answer(text="На ближайшее время нет событийю\n"
                                  "Нажмите на /menu, чтобы вернуться в начало")
    else:
        await message.answer(text='Список ближайших событий', reply_markup=events_menu)


@dp.callback_query_handler(text='back')
async def back(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.edit_text(text='Что тебя интересует ?')
    await call.message.edit_reply_markup(reply_markup=main_menu)


@dp.callback_query_handler(subject_choice_callback.filter())
async def choose_subject(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    logging.info(f"call = {callback_data}")
    subject = callback_data.get('subject_name')
    await call.message.answer(
        text='\n'.join([key.rstrip("_link").title() + ": " + value for key, value in subjects_dict[subject].items()])
    )


@dp.callback_query_handler(social_media_choice_callback.filter())
async def choose_social_media(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    logging.info(f"call = {callback_data}")
    social_media = callback_data.get('social_media_name')
    social_media_dict[social_media]["clicks"] += 1
    await call.message.answer(
        text=f"Ссылка на {social_media}: \n"
             f"{social_media_dict[social_media]['url']}"
    )


@dp.callback_query_handler(event_choice_callback.filter())
async def choose_event(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    logging.info(f"call = {callback_data}")
    date, time = call.data.split(";")[2:]
    await call.message.answer(text=events_dict[date][time]["event_text"])


# adding new subject
@dp.message_handler(commands=["add_subject"], state=None)
async def add_subject(message: Message):
    if await is_admin(message):
        await Subject.subject_name.set()
        await message.answer("Введи название предмета")
    else:
        await message.answer(text="Вы не являетесь админом")


@dp.message_handler(state=Subject.subject_name)
async def add_subject_name(message: Message, state: FSMContext):
    if message.text in subjects_dict:
        await message.answer(text="Такой предмет уже есть!")
        await state.reset_state()
    else:
        async with state.proxy() as data:
            data['subject_name'] = message.text

        await Subject.next()
        await message.answer("Теперь введи ссылку на Instagram-плейлист")


@dp.message_handler(state=Subject.instagram_link)
async def add_instagram_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['instagram_link'] = message.text

    await Subject.next()
    await message.answer("Теперь введи ссылку на чат")


@dp.message_handler(state=Subject.chat_link)
async def add_instagram_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat_link'] = message.text

    await Subject.next()
    await message.answer("И, наконец, введи ссылку на zoom")


@dp.message_handler(state=Subject.zoom_link)
async def add_zoom_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['zoom_link'] = message.text

    await add_subject_json(state)
    await state.finish()

    await message.answer(text=f"Предмет \"{data['subject_name']}\" успешно добавлен")


async def add_subject_json(state: FSMContext):
    async with state.proxy() as data:
        keys = list(data.keys())
        subjects_dict[data[keys[0]]] = {keys[i]: data[keys[i]] for i in range(1, 4)}

    with open("subjects.json", "w") as subjects_file:
        json.dump(subjects_dict, subjects_file, indent=4, ensure_ascii=False)
    global subjects_menu
    subjects_menu = make_subjects_menu()


# ---

# adding new event
@dp.message_handler(commands=['add_event'], state=None)
async def set_event(message: Message):
    if await is_admin(message):
        await Event.event_name.set()
        await message.answer("Введи название события")
    else:
        await message.answer("Вы не являетесь админом")


@dp.message_handler(state=Event.event_name)
async def add_event_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_name'] = message.text

    await Event.next()
    await message.answer("Теперь введи текст рассылки")


@dp.message_handler(state=Event.event_text)
async def add_event_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_text'] = message.text

    await Event.next()
    await message.answer(
        "Теперь введи дату события. Формат: \"dd.mm.yyyy\""
    )


@dp.message_handler(state=Event.event_date)
async def add_event_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_date'] = message.text

    await Event.next()
    await message.answer(
        "И последнее - введи время начала события. Формат: \"hh:mm\""
    )


@dp.message_handler(state=Event.event_time)
async def add_event_time(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_time'] = message.text

    await add_event_json(state)
    await state.finish()
    await message.answer(
        f"Событие \"{data['event_name']}\" с текстом:\n \"{data['event_text']}\"\n"
        f"добавлено и будет разослано за сутки до {data['event_date']}"
        f" в {data['event_time']}"
    )


async def add_event_json(state: FSMContext):
    global events_menu
    async with state.proxy() as data:
        keys = list(data.keys())
        date = data[keys[2]]
        time = data[keys[3]]
        if date not in events_dict:
            events_dict[date] = {}
        events_dict[date][time] = {keys[i]: data[keys[i]] for i in (0, 1)}
        events_dict[date][time]['active'] = True
    with open("events.json", "w") as events_file:
        json.dump(events_dict, events_file, indent=4, ensure_ascii=False)

    events_menu = make_events_menu()


# ---


# notifier
async def notifier():
    global events_menu
    while True:
        date, time = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M").split()

        if events_dict.get(date):
            for event_time in events_dict.get(date):
                if time == event_time and events_dict[date][time]['active']:
                    await bot.send_message(chat_id=OPTIMUM_CHAT_ID,
                                           text=events_dict.get(date).get(event_time).get('event_text'))

                    events_dict[date][time]['active'] = False

                    with open("events.json", "w") as events_file:
                        json.dump(events_dict, events_file, indent=4, ensure_ascii=False)
                    events_menu = make_events_menu()

        await asyncio.sleep(5)


async def is_admin(message: Message):
    user_id = message.from_user.id
    data = await bot.get_chat_administrators(OPTIMUM_CHAT_ID)
    admins_id = [admin["user"]["id"] for admin in data]
    return user_id in admins_id
