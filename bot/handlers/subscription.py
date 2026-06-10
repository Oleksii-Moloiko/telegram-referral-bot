import os

from aiogram import Router, F
from aiogram.types import Message

from bot.services.subscriptions import is_user_channel_member
from bot.services.users import (
    get_or_create_user,
    activate_user_referral,
    get_referrals_count,
)
from bot.services.messages import build_profile_text


router = Router()

CHANNEL_ID = os.getenv("CHANNEL_ID")
BOT_USERNAME = os.getenv("BOT_USERNAME")


@router.message(F.text == "✅ Перевірити підписку")
async def check_subscription_handler(message: Message):
    user, created = await get_or_create_user(message)

    is_member = await is_user_channel_member(
        bot=message.bot,
        channel_id=CHANNEL_ID,
        user_id=message.from_user.id,
    )

    if not is_member:
        await message.answer(
            "Поки не бачу підписки на канал. "
            "Підпишіться, будь ласка, і натисніть кнопку ще раз."
        )
        return

    await activate_user_referral(user)

    referrals_count = await get_referrals_count(user)

    profile_text = build_profile_text(
        user=user,
        referrals_count=referrals_count,
        bot_username=BOT_USERNAME,
    )

    await message.answer(
        "Готово ✅ Підписку підтверджено.\n\n"
        f"{profile_text}"
    )