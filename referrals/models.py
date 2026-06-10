from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(
        unique=True,
        db_index=True
    )

    username = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    joined_channel = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.telegram_id}"


class Referral(models.Model):
    inviter = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="referrals"
    )

    invited = models.OneToOneField(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="invited_by"
    )

    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inviter} -> {self.invited}"