from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import subject_choice_callback, social_media_choice_callback
from db import subjects_dict

# start menu
main_menu = InlineKeyboardMarkup(row_width=2)
social_media_button = InlineKeyboardButton(text="Социальные сети",
                                           callback_data="social media")
subject_button = InlineKeyboardButton(text='Предметы',
                                      callback_data="subjects")
main_menu.insert(social_media_button)
main_menu.insert(subject_button)

# back to previous step
back_button = InlineKeyboardButton(text="Назад", callback_data="back")

# social media

social_media_menu = InlineKeyboardMarkup(row_width=3)
vk = InlineKeyboardButton(text='Вконтакте',
                          callback_data=social_media_choice_callback.new(social_media_name="Вконтакте"))
telegram = InlineKeyboardButton(text='Telegram',
                                callback_data=social_media_choice_callback.new(social_media_name="Telegram"))
instagram = InlineKeyboardButton(text='Instagram',
                                 callback_data=social_media_choice_callback.new(social_media_name="Instagram"))

social_media_menu.add(vk, telegram, instagram)
social_media_menu.insert(back_button)

# subjects
subjects_menu = InlineKeyboardMarkup(row_width=3)
for subject in subjects_dict:
    choose_subject = InlineKeyboardButton(text=subject,
                                          callback_data=subject_choice_callback.new(
                                              subject_name=subject,
                                          ))
    subjects_menu.insert(choose_subject)
subjects_menu.insert(back_button)
