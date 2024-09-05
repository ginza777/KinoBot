from telegram.bot import Bot
# from .models import BotToken
from django.db import OperationalError, DatabaseError, ProgrammingError
telegram_token = "7015018136:AAEsRZOz4CN8pRwu56vmLJRbe23IyALWoig"  # Default token
#
# try:
#     if BotToken.objects.exists():
#         telegram_token = BotToken.objects.first().token
# except (OperationalError, DatabaseError, ProgrammingError):
#     # Ignore the error and continue using the default token if table doesn't exist or there's any error
#     pass

bot_dp = Bot(telegram_token)
