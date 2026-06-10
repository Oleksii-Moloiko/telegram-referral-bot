import os
import sys
import asyncio

from pathlib import Path
from dotenv import load_dotenv

# BASE
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# ENV
load_dotenv()

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

# Django init
import django
django.setup()

# IMPORTS after setup
from aiogram import Bot, Dispatcher

from bot.handlers.start import router as start_router
from bot.handlers.profile import router as profile_router
from bot.handlers.subscription import router as subscription_router
from bot.handlers.help import router as help_router


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(profile_router)
dp.include_router(subscription_router)
dp.include_router(help_router)
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
