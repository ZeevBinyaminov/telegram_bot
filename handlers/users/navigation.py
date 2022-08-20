import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.choice_buttons import choice, calculus_keyboard
from loader import dp


# обработка команды

@dp.message_handler(Command("items"))  # /items
async def show_items(message: Message):
    await message.answer(text="Выбери интересующий предмет:",
                         reply_markup=choice)


# обработка нажатия на кнопку

@dp.callback_query_handler(text_contains="Calculus")
async def choose_calculus(call: CallbackQuery):
    await call.answer(cache_time=10)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Ссылка на матан:", reply_markup=calculus_keyboard)



