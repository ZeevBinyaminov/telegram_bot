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
subjects_menu = InlineKeyboardMarkup(row_width=3)


#
# for subject in subjects_dict:
#     choose_subject = InlineKeyboardButton(text=subject,
#                                           callback_data=subject_choice_callback.new(
#                                               subject_name=subject,
#                                           ))
#     subjects_menu.insert(choose_subject)
# subjects_menu.insert(back_button)
def update_subjects_menu():
    global subjects_menu, subjects_dict
    subjects_menu = InlineKeyboardMarkup(row_width=3)
    for subject in subjects_dict:
        choose_subject = InlineKeyboardButton(text=subject,
                                              callback_data=subject_choice_callback.new(
                                                  subject_name=subject,
                                              ))
        subjects_menu.insert(choose_subject)
    subjects_menu.insert(back_button)


update_subjects_menu()

# events
events_menu = InlineKeyboardMarkup(row_width=1)


def update_events_menu():
    from db import events_dict
    global events_menu
    events_menu = InlineKeyboardMarkup(row_width=1)
    sorted_dates = sorted(events_dict, key=lambda date: datetime.strptime(date, '%d.%m.%Y'))
    for event_date in sorted_dates:
        sorted_time = sorted(events_dict[event_date], key=lambda date: datetime.strptime(date, '%H:%M'))
        for event_time in sorted_time:
            choose_event = InlineKeyboardButton(
                text=f"{events_dict[event_date][event_time]['event_name']}: {event_date} - {event_time}",
                callback_data=event_choice_callback.new(
                    event_name=events_dict[event_date][event_time]['event_name'],
                )
            )
            events_menu.insert(choose_event)
    events_menu.insert(back_button)


update_events_menu()
