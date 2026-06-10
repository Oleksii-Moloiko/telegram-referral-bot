import os

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Мій профіль")],
        [KeyboardButton(text="✅ Перевірити підписку")],
        [KeyboardButton(text="🏆 Рейтинг")],
    ],
    resize_keyboard=True,
)


def get_subscription_keyboard():
    channel_url = os.getenv("CHANNEL_URL")

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Перейти в канал",
                    url=channel_url,
                )
            ]
        ]
    )