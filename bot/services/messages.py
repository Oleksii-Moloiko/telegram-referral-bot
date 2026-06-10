def build_profile_text(user, referrals_count, bot_username):
    referral_link = f"https://t.me/{bot_username}?start={user.telegram_id}"

    subscription_status = (
        "підтверджено ✅"
        if user.joined_channel
        else "не підтверджено ❌"
    )

    return (
        f"Ваш профіль:\n\n"
        f"Статус підписки: {subscription_status}\n\n"
        f"Ваше реферальне посилання:\n"
        f"{referral_link}\n\n"
        f"Запрошено: {referrals_count}"
    )