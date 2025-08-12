import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

TOKEN = os.getenv("BOT_TOKEN")
