from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from ..apps import BotConfig
from . import webhook


def index(request):
    return JsonResponse({"error": "sup hacker"})


urlpatterns = [
    path('', index, name="index"),
    path(f'{BotConfig.app_url}/bot/<str:bot_token>', csrf_exempt(webhook.TelegramBotWebhookView.as_view())),
]


__all__ = ["urlpatterns"]