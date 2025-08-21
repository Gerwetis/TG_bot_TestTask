import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")
AUTH_KEY = os.environ.get("AUTH_KEY", "").strip()

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set!")
