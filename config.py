# config.py
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

# NewsAPI.org API Key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("NEWSAPI_KEY environment variable not set.")