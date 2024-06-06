import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from telegram import Bot
from telegram.ext import Updater
from django.conf import settings
import requests


token=input("Enter the token: ")


from bots.common_bot.dispatcher import setup_dispatcher
url = f"https://api.telegram.org/bot{token}/deleteWebhook"
requests.post(url)


def run_polling(tg_token: str = settings.CAPTION_BOT_TOKEN):
    """ Run bot in polling mode """
    updater = Updater(tg_token, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(tg_token).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_polling()
