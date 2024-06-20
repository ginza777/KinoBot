import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from telegram import Bot
from telegram import Update
from telegram.ext import Dispatcher

from core.celery import app
from ..dispatcher import setup_dispatcher

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def process_telegram_event(update_json, bot_token):
    bot = Bot(bot_token)
    print("update_json: ", update_json)
    update = Update.de_json(update_json, bot)
    n_workers = 4 if settings.DEBUG else 8
    dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
    dispatcher.process_update(update)


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, bot_token, *args, **kwargs):
        if settings.DEBUG:
            process_telegram_event(json.loads(request.body), bot_token)
        else:
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)!
            # Locally, You can run all of these services via docker-compose.yml
            process_telegram_event.delay(json.loads(request.body),bot_token)

        # e.g. remove buttons, typing event
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})
