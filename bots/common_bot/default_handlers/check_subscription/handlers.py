from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext

from . import keyboard
from . import static_text
from ...models import User
from ...main_bot.bot import Bot_settings

def ask_subscribe_channel(update, context):
    u, created = User.get_user_and_created(update, context)

    update.message.reply_text(static_text.subscribe_channel_text,
                              reply_markup=keyboard.keyboard_check_subscription_channel())


def add_ask_subscribe_channel(func):

    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        u, created = User.get_user_and_created(update, context)
        kwargs['subscribe'] = True
        if Bot_settings().force_channels():
            reply_markup, subscribed_status = keyboard.keyboard_checked_subscription_channel(u.user_id)
            kwargs['subscribe'] = subscribed_status  # Pass the subscribe status to the wrapped function
            if subscribed_status:
                return func(update, context, *args, **kwargs)
            else:
                update.message.reply_text(static_text.subscribe_channel_text,
                                          reply_markup=keyboard.keyboard_check_subscription_channel())

        return func(update, context, *args, **kwargs)

    return wrapper

def check_subscription_channel(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    query = update.callback_query
    reply_markup, subscribed_status = keyboard.keyboard_checked_subscription_channel(u.user_id)
    try:
        if query.message.reply_markup == reply_markup:
            return
        elif query.message.reply_markup != reply_markup:
            if subscribed_status:
                # Edit message text if the reply markup has changed and the user is subscribed
                query.edit_message_text(static_text.full_permission)
            else:
                # Edit reply markup if the reply markup has changed and the user is not subscribed
                query.edit_message_reply_markup(reply_markup)
    except Exception as e:
        return


def check_subscription_channel_always(func):
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        u, created = User.get_user_and_created(update, context)
        if Bot_settings().force_channels() and Bot_settings().force_channels_always:
            reply_markup, subscribed_status = keyboard.keyboard_checked_subscription_channel(u.user_id)
            if subscribed_status:
                return func(update, context, *args, **kwargs)
            else:
                update.message.reply_text(static_text.subscribe_channel_text,
                                          reply_markup=keyboard.keyboard_check_subscription_channel())
                return
        return func(update, context, *args, **kwargs)

    return wrapper


