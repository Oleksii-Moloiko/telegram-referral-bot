import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if value:
        value = value.strip()

    if not value:
        raise RuntimeError(f"{name} is not set. Please add it to your .env file.")

    return value


BOT_TOKEN = get_required_env("BOT_TOKEN")
BOT_USERNAME = get_required_env("BOT_USERNAME")
CHANNEL_ID = get_required_env("CHANNEL_ID")
CHANNEL_URL = get_required_env("CHANNEL_URL")
ADMIN_TELEGRAM_ID = int(get_required_env("ADMIN_TELEGRAM_ID"))