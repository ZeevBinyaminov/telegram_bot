import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.choice_buttons import choice, calculus_keyboard
from loader import dp


# обработка команды
@dp.message_handler(Command("start"))
async def welcome(message: Message):
    await message.answer(
        text="Привет!\n"
        "Я - бот-навигатор, помогаю найти необходимые ссылки и чаты.\n"
        "Выбери, какой предмет тебя интересует:",
        reply_markup=choice
    )

@dp.message_handler(Command("items"))  # /items
async def show_items(message: Message):
    await message.answer(text="Выбери интересующий предмет:",
                         reply_markup=choice)


# обработка нажатия на кнопку

@dp.callback_query_handler(text_contains="Матан")
async def choose_calculus(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.edit_reply_markup(reply_markup=calculus_keyboard)


@dp.callback_query_handler(text="back to start")
async def back_to_start(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=choice)
