from django.contrib import admin

from .models import TelegramUser, Referral


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "username",
        "first_name",
        "joined_channel",
        "created_at",
    )
    search_fields = (
        "telegram_id",
        "username",
        "first_name",
    )
    list_filter = (
        "joined_channel",
        "created_at",
    )


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = (
        "inviter",
        "invited",
        "active",
        "created_at",
    )
    search_fields = (
        "inviter__telegram_id",
        "invited__telegram_id",
        "inviter__username",
        "invited__username",
    )
    list_filter = (
        "active",
        "created_at",
    )