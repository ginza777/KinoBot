from django.conf import settings

from . import models
from ..apps import BotConfig


class Bot_settings:
    webhook_url = f"{settings.WEBHOOK_URL}/{BotConfig.app_url}/bot/"

    def force_channels(self):
        try:
            status = models.Channel.get_channel_count_status()
        except:
            status = False
        return status

    # forces users to enter channels always
    force_channels_always = True
    # adds a language selection command after start
    force_language = False
    # adds a location request command after start
    # force_location = False
