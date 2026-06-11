import logging
from asgiref.sync import sync_to_async

from referrals.models import TelegramUser, Referral

logger = logging.getLogger(__name__)

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
        logger.info(
            "Referral skipped: invited user already exists user_id=%s",
            invited_user.telegram_id,
        )
        return "already_exists"

    if not inviter_telegram_id:
        logger.info(
            "Referral skipped: no inviter payload user_id=%s",
            invited_user.telegram_id,
        )
        return "no_payload"

    try:
        inviter_telegram_id = int(inviter_telegram_id)
    except ValueError:
        logger.info(
            "Referral skipped: invalid inviter payload payload=%s user_id=%s",
            inviter_telegram_id,
            invited_user.telegram_id,
        )
        return "invalid_payload"

    if invited_user.telegram_id == inviter_telegram_id:
        logger.info(
            "Referral skipped: self referral user_id=%s",
            invited_user.telegram_id,
        )
        return "self_referral"

    try:
        inviter = TelegramUser.objects.get(
            telegram_id=inviter_telegram_id
        )
    except TelegramUser.DoesNotExist:
        logger.info(
            "Referral skipped: inviter not found inviter_id=%s invited_id=%s",
            inviter_telegram_id,
            invited_user.telegram_id,
        )
        return "inviter_not_found"

    referral, created = Referral.objects.get_or_create(
        invited=invited_user,
        defaults={
            "inviter": inviter,
        }
    )

    if created:
        logger.info(
            "Referral created: inviter_id=%s invited_id=%s",
            inviter.telegram_id,
            invited_user.telegram_id,
        )
        return "created"

    logger.info(
        "Referral already exists: invited_id=%s",
        invited_user.telegram_id,
    )
    return "already_has_referral"


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