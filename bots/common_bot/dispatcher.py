"""
    Telegram event handlers
"""
from telegram.ext import (
    CommandHandler, MessageHandler, CallbackQueryHandler, Filters, ConversationHandler)
from django.conf import settings
from telegram.ext.dispatcher import Dispatcher

from . import views
from .default_handlers.admin import handlers as admin_handlers
from .default_handlers.broadcast_message import handlers as broadcast_handlers
from .default_handlers.broadcast_message.handlers import broadcast_command
from .default_handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from .default_handlers.check_subscription import handlers as check_subscription_handlers
from .default_handlers.language import handlers as language_handlers
from .default_handlers.location import handlers as location_handlers
from .default_handlers.onboarding import handlers as onboarding_handlers
from .default_handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from .state import state
from .main_bot.bot import Bot_settings

def setup_dispatcher(dp):
    states = {
        state.ANOTHER: [
            CommandHandler('start', views.start),
        ],
        # you can add more states here

    }

    entry_points = [CommandHandler('start', views.start), ]

    fallbacks = [
        MessageHandler(Filters.all, views.start),
    ]
    conversation_handler = ConversationHandler(
        entry_points=entry_points,
        states=states,
        fallbacks=fallbacks,
        name="conversationbot",
    )


    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    dp.add_handler(conversation_handler)
    dp.add_handler(MessageHandler(Filters.update.channel_posts, onboarding_handlers.ignore_updates))
    dp.add_handler(MessageHandler(Filters.group, onboarding_handlers.ignore_updates))

    dp.add_handler(MessageHandler(Filters.video, views.get_movie_from_admin))
    dp.add_handler(CommandHandler("random_no_trailers_movie", views.random_no_trailers_movie))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex('^\d+$'), views.get_movie_by_code))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🔍 Search Movies"), views.random_no_trailers_movie))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎲 Random Kino"), views.top_movies))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎲 Случайный фильм"), views.top_movies))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎲 Random Movie"), views.top_movies))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎥 Top 1 Kino"), views.top_movies))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎥 Топ 1 фильмов"), views.top_movies))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎥 Top 1 Movies"), views.top_movies))


    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎥 Top 3 Kinolar"), views.top_movies))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎥 Топ 3 Фильмы"), views.top_movies))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🎥 Top 3 Movies"), views.top_movies))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🌍 Change Language"), language_handlers.ask_language))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🌍 Tilni o'zgartirish"), language_handlers.ask_language))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^🌍 Изменить язык"), language_handlers.ask_language))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📚 Help"), onboarding_handlers.help))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📚 Помощь"), onboarding_handlers.help))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📚 Yordam"), onboarding_handlers.help))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📤 Share Bot"), views.share_bot))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📤 Поделиться ботом"), views.share_bot))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📤 Botni ulashish"), views.share_bot))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📞 About Us"), onboarding_handlers.about))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📞 О_нас"), onboarding_handlers.about))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^📞 Biz haqimizda"), onboarding_handlers.about))


    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^перезапуск"), views.start))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^restart"), views.start))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"^boshlash"), views.start))

    """
    Adding handlers for events from Telegram
    """
    dp.add_handler(CommandHandler("start", views.start))

    # location
    dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    dp.add_handler(CommandHandler("backup_db", admin_handlers.backup_db))
    dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))
    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'),
                       broadcast_handlers.broadcast_command_with_message)
    )
    # secret level
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))



    # about help
    dp.add_handler(CommandHandler("help", onboarding_handlers.help))
    dp.add_handler(CommandHandler("about", onboarding_handlers.about))
    dp.add_handler(CommandHandler("language", language_handlers.ask_language))

    # check subscription
    dp.add_handler(
        CallbackQueryHandler(check_subscription_handlers.check_subscription_channel, pattern="^check_subscription"))

    # choice language
    dp.add_handler(CallbackQueryHandler(language_handlers.language_choice_handle, pattern="^language_setting_"))

    return dp


