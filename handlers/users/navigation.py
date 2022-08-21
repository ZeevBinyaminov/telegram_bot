import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.choice_buttons import main_menu, social_media_menu, subjects_menu
from keyboards.inline.callback_data import subject_choice_callback, social_media_choice_callback, navigation_callback
from loader import dp

from info import subjects_dict, social_media_dict


# обработка команды
@dp.message_handler(Command("start"))
async def welcome(message: Message):
    await message.answer(
        text="Привет!\n"
             "Я - бот-навигатор, помогаю найти необходимые ссылки и чаты.\n"
             "Что ебя интересует ?",
        reply_markup=main_menu
    )


@dp.message_handler(Command("items"))  # /items
async def show_items(message: Message):
    await message.answer(text='Что тебя интересует ?', reply_markup=main_menu)


@dp.callback_query_handler(text='social media')
async def choose_social_media(call: CallbackQuery):
    await call.answer(cache_time=3)
    logging.info(f"call = {call.data}")
    await call.message.answer(text='Наши соцсети:', reply_markup=social_media_menu)


@dp.callback_query_handler(text='subjects')
async def choose_subjects(call: CallbackQuery):
    await call.answer(cache_time=1)
    logging.info(f"call = {call.data}")
    await call.message.answer(text='Выбери предмет:', reply_markup=subjects_menu)


@dp.callback_query_handler(text='back')
async def choose_subjects(call: CallbackQuery):
    await call.answer(cache_time=1)
    logging.info(f"call = {call.data}")
    await call.message.answer(text='Что тебя интересует ?', reply_markup=main_menu)




# выбор одного из предметов
@dp.callback_query_handler(text='subjects')
async def choose_subject(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    # callback_data = call.data
    logging.info(f"call = {callback_data}")
    subject = callback_data.get('subject_name')

    if subjects_dict.get(subject):
        await call.message.answer(text=subjects_dict[subject])
    else:
        await call.message.answer(text=f'Your text: {subject}')
