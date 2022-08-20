import logging

from aiogram import Bot, Dispatcher

import config

bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)