# env
from telegram import Bot
import requests


def set_webhook_single(bot_token, webhook_url):
    url = (
        f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/{bot_token}"
    )
    response = requests.post(url)
    return response


def get_bot_info_single(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    print(response.json())
    return response.json().get("result").get("username"), response.json().get("result").get("first_name")


def check_bot_status_admin(channel_id, telegram_token):
    try:
        bot = Bot(telegram_token)
        admins = bot.get_chat_administrators(channel_id)
        bot_id = bot.get_me().id
        bot_is_admin = any(admin.user.id == bot_id for admin in admins)
        return bot_is_admin
    except Exception as e:
        print("Error in check_bot_status_admin: ", e)
        return False


__all__ = ["set_webhook_single", "get_bot_info_single", "check_bot_status_admin"]
