from django.apps import AppConfig
from django.core.management import call_command

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bots.common_bot'
    app_url = name.split('.')[1]


    # def ready(self):
    #     # Run the set_webhook management command
    #     call_command('set_webhook')
