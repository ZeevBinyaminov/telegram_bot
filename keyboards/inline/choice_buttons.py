from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import subject_choice_callback, social_media_choice_callback, event_choice_callback
from db import subjects_dict, events_dict

# start menu
main_menu = InlineKeyboardMarkup(row_width=2)
social_media_button = InlineKeyboardButton(text="Социальные сети",
                                           callback_data="social media")
subject_button = InlineKeyboardButton(text='Предметы',
                                      callback_data="subjects")
events_button = InlineKeyboardButton(text='События', callback_data="events")

main_menu.insert(social_media_button)
main_menu.insert(subject_button)
main_menu.insert(events_button)
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

def make_subjects_menu():
    menu = InlineKeyboardMarkup(row_width=3)
    for subject in subjects_dict:
        choose_subject = InlineKeyboardButton(text=subject,
                                              callback_data=subject_choice_callback.new(
                                                  subject_name=subject,
                                              ))
        menu.insert(choose_subject)
    menu.insert(back_button)
    return menu


subjects_menu = make_subjects_menu()


# events

def make_events_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    is_empty = True
    sorted_dates = sorted(events_dict, key=lambda date: datetime.strptime(date, '%d.%m.%Y'))
    for event_date in sorted_dates:
        sorted_time = sorted(events_dict[event_date], key=lambda date: datetime.strptime(date, '%H:%M'))
        for event_time in sorted_time:
            if events_dict[event_date][event_time]['active']:
                is_empty = False
                choose_event = InlineKeyboardButton(
                    text=f"{events_dict[event_date][event_time]['event_name']}: {event_date} - {event_time}",
                    callback_data=event_choice_callback.new(
                        event_name=events_dict[event_date][event_time]['event_name'],
                    )
                )
                menu.insert(choose_event)
    if not is_empty:
        menu.insert(back_button)
    return menu


events_menu = make_events_menu()
