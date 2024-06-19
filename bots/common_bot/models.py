import requests
from django.core.exceptions import ValidationError
from django.db import models

from utils.models import CreateTracker, nb
from .main_bot.function import *  # noqa
from .main_bot.models import *  # noqa


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


class MovieTrailer(CreateTracker):
    file_unique_id = models.CharField(max_length=64, unique=True)
    metadata = models.JSONField(**nb)

    def __str__(self):
        return str(self.file_unique_id)


class Movie(CreateTracker):
    file_unique_id = models.CharField(max_length=64, unique=True)
    caption = models.TextField(**nb)
    code = models.IntegerField(default=0)
    metadata = models.JSONField(**nb)
    view_count = models.IntegerField(default=0)
    trailer = models.ForeignKey(MovieTrailer, on_delete=models.CASCADE, null=True, blank=True, related_name="trailer")
    has_trailer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file_unique_id)

    def save(self, *args, **kwargs):
        if self.trailer:
            self.has_trailer = True
        else:
            self.has_trailer = False
        super(Movie, self).save(*args, **kwargs)


class MovieChannel(CreateTracker):
    channel_id = models.CharField(max_length=64, unique=True)
    channel_username = models.CharField(max_length=64, unique=True)
    active = models.BooleanField(default=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.channel_id)

    def save(self, *args, **kwargs):
        if not self.channel_username.startswith("@") and not self.channel_username.startswith(
                "https://t.me/") and not self.private:
            self.channel_username = "@" + self.channel_username
        if self.channel_usernaxme.startswith("https://t.me/") and not self.private:
            self.channel_username = self.channel_username.replace("https://t.me/", "@")
        if not self.channel_id.startswith("-100"):
            self.channel_id = "-100" + self.channel_id

        super(MovieChannel, self).save(*args, **kwargs)

    def clean(self):
        status = check_bot_status_admin(self.channel_id)
        if not status:
            raise ValidationError("Bot is not admin in the channel")


class Unnecessary_word_filter(CreateTracker):
    word = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.word)


class SuperSettings(CreateTracker):
    movie_channel_username= models.CharField(max_length=64, unique=True)
    movie_bot_username= models.CharField(max_length=64, unique=True)
    trailer_channel_id= models.IntegerField(unique=True,default="-1002080046544")

    def __str__(self):
        return  "SuperSetttings"


