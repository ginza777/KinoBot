from telegram import Update
from telegram.ext import CallbackContext

from .keyboard import language_list_keyboard
from .static_text import ask_language_text,choice_language,restart_text
from ...keyboard.keyboard import restart_keyboard
from ...models import User


def ask_language(update, context) -> None:
    u, created = User.get_user_and_created(update, context)
    lang = u.selected_language
    """ Entered /ask_location command"""
    update.message.reply_text(ask_language_text[lang], reply_markup=language_list_keyboard())


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
    update.callback_query.answer(f"{choice_language[lang_id]} {Language[lang_id]}")
    query.edit_message_text(f"{choice_language[lang_id]} {Language[lang_id]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{restart_text[lang_id]}",reply_markup=restart_keyboard(lang=lang_id))
