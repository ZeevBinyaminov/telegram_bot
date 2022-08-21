import json

with open("users.json", "r") as users_file:
    users_dict = json.load(users_file)

with open("subjects.json", "r") as subjects_file:
    subjects_dict = json.load(subjects_file)

with open("social_media.json", "r") as social_media_file:
    social_media_dict = json.load(social_media_file)
