import os
# загрузка переменных окружения из специального файла
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")