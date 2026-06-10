import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.users import (
    get_or_create_user,
    get_referrals_count,
)
from bot.services.messages import build_profile_text


router = Router()

BOT_USERNAME = os.getenv("BOT_USERNAME")


@router.message(Command("profile"))
async def profile_handler(message: Message):
    user, created = await get_or_create_user(message)

    referrals_count = await get_referrals_count(user)

    text = build_profile_text(
        user=user,
        referrals_count=referrals_count,
        bot_username=BOT_USERNAME,
    )

    await message.answer(text)


@router.message(F.text == "👤 Мій профіль")
async def profile_button_handler(message: Message):
    await profile_handler(message)