import logging
import config
from aiogram import Bot, Dispatcher
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage

loop = asyncio.get_event_loop()
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)

logging.basicConfig(level=logging.INFO)