from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import choice_callback

subjects = {
    "Calculus": "https://vk.com",
    "Linear_algebra": "https://youtube.com",
}

# choice = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Матан", callback_data=choice_callback.new(
#                 subject_name="Calculus", link="https://www.youtube.com/watch?v=qP3cop0GTvU"
#             )),
#             # InlineKeyboardButton(text="Тервер", callback_data="")
#         ],
#         [
#             InlineKeyboardButton(text="Отмена", callback_data="cancel")
#         ]
#     ]
# )

choice = InlineKeyboardMarkup(row_width=2)
for subject in sorted(subjects):
    choose_subject = InlineKeyboardButton(text=subject,
                                          callback_data=choice_callback.new(
                                              subject_name=subject,
                                              link='https://youtube.com'
                                          ))
    choice.insert(choose_subject)

calculus_keyboard = InlineKeyboardMarkup()
calculus_keyboard.insert(InlineKeyboardButton(text='youtube', url='https://youtube.com'))
