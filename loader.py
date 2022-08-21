import logging
import config
from aiogram import Bot, Dispatcher

bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)