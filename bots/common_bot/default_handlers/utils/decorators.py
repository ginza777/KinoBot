from functools import wraps
from typing import Callable

from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from ...models import User


def admin_only(func: Callable):
    """
    Admin only decorator
    Used for handlers that only admins have access to
    """

    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if update.message:
            user = User.get_user(update, context)
        else:
            return

        if not user.is_admin:
            update.message.reply_text("You are not an admin!")
            return

        return func(update, context, *args, **kwargs)

    return wrapper


def check_channel(func: Callable):
    """
    Admin only decorator
    Used for handlers that only admins have access to
    """

    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if update.message:
            user = User.get_user(update, context)
        else:
            return

        return func(update, context, *args, **kwargs)

    return wrapper


def send_typing_action(func: Callable):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update: Update, context: CallbackContext, *args, **kwargs):
        update.effective_chat.send_chat_action(ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func
