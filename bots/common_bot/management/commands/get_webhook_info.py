import requests
from django.core.management.base import BaseCommand

from ...main_bot.bot import Bot_settings
from ...models import BotToken

webhook_url = Bot_settings.webhook_url
token_list = BotToken.objects.all().values_list("token", flat=True)


def get_bot_webhook_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    r = requests.post(url)
    return r.json()


def get_bot_info_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    return response.json().get("result").get("username"), response.status_code, url


def get_webhook():
    if len(token_list) == 0:
        print("No bots found")
        return
    for bot in token_list:
        username, res, url = get_bot_info_single(bot)
        print("\n\n", 100 * "-")
        print("webhook info get for bot:", f"https://t.me//{username}")
        print("token:", bot, "status:", res)
        print("webhook url:", get_bot_webhook_single(bot).get("result").get("url"))
        print("get_url:", url)
    print("Get webhook info successfully for all bots\n\n")


class Command(BaseCommand):
    help = "Set webhook for all bots"

    def handle(self, *args, **options):
        get_webhook()
