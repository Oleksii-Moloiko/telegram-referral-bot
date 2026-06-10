import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.services.users import (
    get_or_create_user,
    create_referral,
)
from bot.keyboards.menu import main_menu, get_subscription_keyboard


router = Router()

BOT_USERNAME = os.getenv("BOT_USERNAME")


@router.message(CommandStart())
async def start_handler(message: Message):
    user, created = await get_or_create_user(message)

    command_parts = message.text.split(maxsplit=1)
    inviter_telegram_id = command_parts[1] if len(command_parts) > 1 else None

    await create_referral(
        invited_user=user,
        inviter_telegram_id=inviter_telegram_id,
    )

    await message.answer(
        "Вітаю 👋\n\n"
        "Щоб активувати участь у реферальній програмі, "
        "підпишіться на канал, а потім натисніть кнопку "
        "«✅ Перевірити підписку».",
        reply_markup=main_menu,
    )

    await message.answer(
        "Канал тут 👇",
        reply_markup=get_subscription_keyboard(),
    )