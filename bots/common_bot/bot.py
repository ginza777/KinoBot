from telegram.bot import Bot
from .models import BotToken
from django.db import OperationalError, DatabaseError, ProgrammingError
telegram_token=''
try:
    if BotToken.objects.exists():
        telegram_token = BotToken.objects.first().token
    else:
        telegram_token = "7015018136:AAEsRZOz4CN8pRwu56vmLJRbe23IyALWoig"
except (OperationalError, DatabaseError, ProgrammingError):
    # Handle the case where the table does not exist or there is another database error
    telegram_token = "7015018136:AAEsRZOz4CN8pRwu56vmLJRbe23IyALWoig"

bot_dp = Bot(telegram_token)
