from telegram.bot import Bot

from .models import BotToken

if BotToken.objects.all().count() > 0:
    telegram_token = BotToken.objects.all().first().token
else:
    telegram_token = "7015018136:AAEsRZOz4CN8pRwu56vmLJRbe23IyALWoig"
bot_dp = Bot(telegram_token)