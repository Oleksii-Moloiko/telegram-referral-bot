from asgiref.sync import sync_to_async

from referrals.models import TelegramUser, Referral


@sync_to_async
def get_or_create_user(message):
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
        }
    )

    return user, created


@sync_to_async
def create_referral(invited_user, inviter_telegram_id, invited_user_was_created):
    if not invited_user_was_created:
        return None

    if not inviter_telegram_id:
        return None

    try:
        inviter_telegram_id = int(inviter_telegram_id)
    except ValueError:
        return None

    if invited_user.telegram_id == inviter_telegram_id:
        return None

    try:
        inviter = TelegramUser.objects.get(
            telegram_id=inviter_telegram_id
        )
    except TelegramUser.DoesNotExist:
        return None

    referral, created = Referral.objects.get_or_create(
        invited=invited_user,
        defaults={
            "inviter": inviter,
        }
    )

    return referral


@sync_to_async
def get_referrals_count(user):
    return Referral.objects.filter(
        inviter=user,
        active=True,
    ).count()

@sync_to_async
def activate_user_referral(user):
    user.joined_channel = True
    user.save(update_fields=["joined_channel"])

    try:
        referral = Referral.objects.get(invited=user)
    except Referral.DoesNotExist:
        return False

    if referral.active:
        return True

    referral.active = True
    referral.save(update_fields=["active"])

    return True

@sync_to_async
def get_admin_stats():
    users_total = TelegramUser.objects.count()

    users_joined_channel = TelegramUser.objects.filter(
        joined_channel=True,
    ).count()

    referrals_total = Referral.objects.count()

    referrals_active = Referral.objects.filter(
        active=True,
    ).count()

    return {
        "users_total": users_total,
        "users_joined_channel": users_joined_channel,
        "referrals_total": referrals_total,
        "referrals_active": referrals_active,
    }