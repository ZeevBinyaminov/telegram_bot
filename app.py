from aiogram import executor
from config import ADMIN_ID
from loader import bot, storage, loop
from handlers.users.handlers import notifier


async def on_shutdown(dp):
    await bot.send_message(ADMIN_ID, "Бот выключен")
    await storage.close()


async def on_startup(dp):
    await bot.send_message(ADMIN_ID, "Бот запущен")


if __name__ == '__main__':
    from handlers import dp
    loop.create_task(notifier())
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        loop=loop,
        skip_updates=True
    )
