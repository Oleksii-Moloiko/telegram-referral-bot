from django.db.models import Count

from referrals.models import Referral


def get_leaderboard(limit: int = 5):
    return (
        Referral.objects
        .filter(active=True)
        .values(
            "inviter__telegram_id",
            "inviter__username",
            "inviter__first_name",
        )
        .annotate(active_referrals_count=Count("id"))
        .order_by("-active_referrals_count", "inviter__telegram_id")[:limit]
    )


def build_leaderboard_text() -> str:
    leaders = get_leaderboard()

    if not leaders:
        return (
            "🏆 Рейтинг поки порожній.\n\n"
            "Запрошуй друзів через своє реферальне посилання, "
            "і після підтвердження підписки вони зʼявляться у статистиці."
        )

    lines = ["🏆 Топ користувачів за активними запрошеннями:\n"]

    for index, leader in enumerate(leaders, start=1):
        username = leader["inviter__username"]
        first_name = leader["inviter__first_name"]
        telegram_id = leader["inviter__telegram_id"]
        count = leader["active_referrals_count"]

        if username:
            name = f"@{username}"
        elif first_name:
            name = first_name
        else:
            name = f"ID {telegram_id}"

        lines.append(f"{index}. {name} — {count}")

    return "\n".join(lines)