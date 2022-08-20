from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import choice_callback

subjects = {
    "Calculus": "https://vk.com",
    "Linear_algebra": "https://youtube.com",
}


choice = InlineKeyboardMarkup(row_width=2)
for subject in sorted(subjects):
    choose_subject = InlineKeyboardButton(text=subject,
                                          callback_data=choice_callback.new(
                                              subject_name=subject,
                                              link='https://youtube.com'
                                          ))
    choice.insert(choose_subject)

restart_button = InlineKeyboardButton(text="В начало", callback_data="back to start")
back_button = InlineKeyboardButton(text="Назад", callback_data="one turn back")
choice.insert(restart_button)
choice.insert(back_button)

calculus_keyboard = InlineKeyboardMarkup()
calculus_keyboard.insert(InlineKeyboardButton(text='youtube', url='https://youtube.com'))
calculus_keyboard.insert(restart_button)
