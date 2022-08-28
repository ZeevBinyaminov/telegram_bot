from aiogram.utils.callback_data import CallbackData

subject_choice_callback = CallbackData("subject", "subject_name", sep=";")
social_media_choice_callback = CallbackData("social_media", "social_media_name", sep=";")
event_choice_callback = CallbackData("event", "event_Name", "event_Date", "event_Time", sep=";")