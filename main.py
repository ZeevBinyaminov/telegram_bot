import logging
from config import API_TOKEN

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

button1 = KeyboardButton('Hello')
button2 = KeyboardButton('Bye')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True).add(button1).add(button2)


@dp.message_handler(commands=['start'])
async def say_hello(message: types.Message):
    await message.reply('Hello', reply_markup=keyboard)


@dp.message_handler()
async def kb_answer(message: types.Message):
    reply_dict = {'Hello': 'Hi, how are you?',
                  'Bye': 'See you!'}
    reply = reply_dict.get(message.text)
    await message.answer(reply if reply else 'No such button')


if __name__ == '__main__':
    from handlers import dp, send_to_admin

    # фраза при запуске бота в виде функции
    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True)
