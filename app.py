from aiogram import executor
from config import ADMIN_ID
from loader import bot


async def on_shutdown(dp):
    await bot.send_message(ADMIN_ID, "Бот выключен")
    await bot.close()


async def on_startup(dp):
    await bot.send_message(ADMIN_ID, "Бот запущен\n")


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
