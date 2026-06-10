from asgiref.sync import sync_to_async
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.stats import build_leaderboard_text


router = Router()


@router.message(Command("leaderboard"))
async def leaderboard_command(message: Message):
    text = await sync_to_async(build_leaderboard_text)()
    await message.answer(text)