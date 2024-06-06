import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import BotToken
from ...main_bot.bot import Bot_settings

token_list = BotToken.objects.all().values_list("token", flat=True)
webhook_url = Bot_settings.webhook_url


def get_bot_info_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    return response.json().get("result").get("username")


def set_webhook_single(bot_token, webhook_url):
    url_webhook = f"{webhook_url}{bot_token}"
    print("url_webhook", url_webhook)
    url = (
        f"https://api.telegram.org/bot{bot_token}/setWebhook?url={url_webhook}"
    )
    response = requests.post(url)
    return response

def get_bot_webhook_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    r= requests.post(url)
    return r.json()


def set_webhook():
    if len(token_list) == 0:
        print("No bots found")
        return
    for bot in token_list:
        res = set_webhook_single(bot, webhook_url)
        username = get_bot_info_single(bot)
        print("\n\n", 100 * "-")
        print("webhook set for bot:", f"https://t.me//{username}")
        print("token:", bot, "status:", res.status_code)
        print("webhook url:", get_bot_webhook_single(bot).get("result").get("url"))
    print("Webhook set successfully for all bots\n\n")


class Command(BaseCommand):
    help = "Set webhook for all bots"

    def handle(self, *args, **options):
        set_webhook()
