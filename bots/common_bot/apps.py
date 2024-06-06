from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bots.common_bot'
    app_url = name.split('.')[1]
