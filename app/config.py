import os
from dotenv import load_dotenv

# for load local .env datas
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
AUTH_KEY = os.getenv("AUTH_KEY", "").strip()

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set!")
