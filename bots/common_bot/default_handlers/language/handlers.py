from telegram import Update
from telegram.ext import CallbackContext

from .keyboard import language_list_keyboard
from .static_text import ask_language_text
from ...models import User


def ask_language(update, context) -> None:
    """ Entered /ask_location command"""
    update.message.reply_text(ask_language_text, reply_markup=language_list_keyboard())


def language_choice_handle(update: Update, context: CallbackContext):
    Language = {
        "uz": "Uzbek",
        "en": "English",
        "ru": "Russian",
    }
    u, created = User.get_user_and_created(update, context)
    query = update.callback_query
    lang_id = query.data.split("language_setting_")[-1]
    u.selected_language = lang_id
    u.save()
    update.callback_query.answer(f"You choice language is {Language[lang_id]}")
    query.edit_message_text(f"You choice language is {Language[lang_id]}")
