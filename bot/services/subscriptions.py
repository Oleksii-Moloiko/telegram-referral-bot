async def is_user_channel_member(bot, channel_id, user_id):
    try:
        member = await bot.get_chat_member(
            chat_id=channel_id,
            user_id=user_id,
        )

        print("CHANNEL_ID:", channel_id)
        print("USER_ID:", user_id)
        print("MEMBER_STATUS:", member.status)

        return member.status in [
            "member",
            "administrator",
            "creator",
        ]

    except Exception as error:
        print("SUBSCRIPTION CHECK ERROR:", error)
        return False