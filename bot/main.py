import os
import sys
import asyncio
import logging

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

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
from bot.handlers.stats import router as stats_router
from bot.handlers.leaderboard import router as leaderboard_router

from bot.env import BOT_TOKEN, BOT_USERNAME, APP_ENV



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(profile_router)
dp.include_router(subscription_router)
dp.include_router(help_router)
dp.include_router(stats_router)
dp.include_router(leaderboard_router)


async def main():
    logging.info("Starting bot environment=%s username=%s", APP_ENV, BOT_USERNAME)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())