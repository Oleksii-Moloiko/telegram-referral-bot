from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.menu import main_menu


router = Router()


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "Як користуватися ботом:\n\n"
        "1. Підпишіться на канал.\n"
        "2. Натисніть «✅ Перевірити підписку».\n"
        "3. Отримайте своє реферальне посилання.\n"
        "4. Надсилайте його друзям.\n"
        "5. Активними рахуються тільки ті запрошені, які теж підтвердили підписку.\n\n"
        "Команди:\n"
        "/start — почати\n"
        "/profile — мій профіль\n"
        "/help — допомога",
        reply_markup=main_menu,
    )