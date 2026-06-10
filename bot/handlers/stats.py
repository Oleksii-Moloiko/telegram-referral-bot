import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.users import get_admin_stats


router = Router()

ADMIN_TELEGRAM_ID = os.getenv("ADMIN_TELEGRAM_ID")


@router.message(Command("stats"))
async def stats_handler(message: Message):
    if str(message.from_user.id) != ADMIN_TELEGRAM_ID:
        await message.answer("Ця команда доступна тільки адміну.")
        return

    stats = await get_admin_stats()

    await message.answer(
        "Статистика бота:\n\n"
        f"Користувачів всього: {stats['users_total']}\n"
        f"Підписку підтвердили: {stats['users_joined_channel']}\n\n"
        f"Рефералів всього: {stats['referrals_total']}\n"
        f"Активних рефералів: {stats['referrals_active']}"
    )