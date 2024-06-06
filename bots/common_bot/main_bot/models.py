from __future__ import annotations

from typing import Union, Optional, Tuple

import environ
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet, Manager
from telegram import Update
from telegram.ext import CallbackContext

from ..main_bot.bot import Bot_settings

env = environ.Env()
env.read_env(".env")
from .function import check_bot_status_admin
from ..default_handlers.utils.info import extract_user_data_from_update

nb = dict(null=True, blank=True)


class GetOrNoneManager(models.Manager):
    """returns none if object doesn't exist else model instance"""

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class User(models.Model):
    user_id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", **nb)
    selected_language = models.CharField(max_length=8, help_text="Bot's lang", **nb)
    deep_link = models.CharField(max_length=64, **nb)

    is_blocked_bot = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    objects = GetOrNoneManager()  # user = User.objects.get_or_none(user_id=<some_id>)
    admins = AdminUserManager()  # User.admins.all()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_and_created(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            # Save deep_link to User model
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> User:
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @property
    def invited_users(self) -> QuerySet[User]:
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"


class Location(models.Model):
    user = models.ForeignKey('common_bot.User', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GetOrNoneManager()

    def __str__(self):
        return f"user: {self.user}, created at {self.created_at.strftime('(%H:%M, %d %B %Y)')}"


class Channel(models.Model):
    channel_username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    channel_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.channel_username

    class Meta:
        verbose_name = "Channel_for_subscription"
        verbose_name_plural = "Channels_for_subscription"
        ordering = ["-date_created"]

    def save(self, *args, **kwargs):

        if self.channel_username is not None:
            if self.channel_username.startswith("https://t.me/"):
                self.channel_username = self.channel_username.replace("https://t.me/", "")
            if self.channel_username.startswith("@"):
                self.channel_username = self.channel_username.replace("@", "")
        super().save(*args, **kwargs)

    def clean(self):
        if self.channel_username is not None:
            if not check_bot_status_admin(self.channel_id, env("ADMIN_BOT_TOKEN")):
                raise ValidationError("Bot kanal administratori emas.")

    @property
    def get_channel_link(self):
        return f"https://t.me/{self.channel_username}"

    def get_channel_count_status(*args, **kwargs):
        if Channel.objects.filter(active=True).count() > 0:
            return True
        else:
            return False


class BotToken(models.Model):
    name = models.CharField(max_length=100,**nb)
    username = models.CharField(max_length=100, **nb)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        username, name = bot_info_single(self.token)
        self.name = name
        self.username = username
        set_webhook_single(self.token, Bot_settings.webhook_url)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "BotToken"
        verbose_name_plural = "BotTokens"


def set_webhook_single(bot_token, webhook_url):
    url = (
        f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/{bot_token}"
    )
    response = requests.post(url)
    return response


def bot_info_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                result = data.get("result")
                if result:
                    username = result.get("username")
                    first_name = result.get("first_name")
                    return username, first_name
                else:
                    print("Response does not contain 'result' field")
            else:
                print("API returned error:", data.get("description"))
        else:
            print("Request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))


__all__ = ["User", "Location", "Channel", "BotToken"]
