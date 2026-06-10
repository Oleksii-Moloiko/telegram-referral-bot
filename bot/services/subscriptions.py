import logging


logger = logging.getLogger(__name__)


async def is_user_channel_member(bot, channel_id, user_id):
    try:
        member = await bot.get_chat_member(
            chat_id=channel_id,
            user_id=user_id,
        )

        logger.info(
            "Subscription check: channel_id=%s user_id=%s status=%s",
            channel_id,
            user_id,
            member.status,
        )

        return member.status in [
            "member",
            "administrator",
            "creator",
        ]

    except Exception as error:
        logger.warning(
            "Subscription check failed: channel_id=%s user_id=%s error=%s",
            channel_id,
            user_id,
            error,
        )
        return False