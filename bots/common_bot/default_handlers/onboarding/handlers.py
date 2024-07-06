import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from . import static_text
from .keyboards import make_keyboard_for_start_command, make_keyboard_for_help_command, make_keyboard_for_about_command, \
    make_keyboard_for_about_command_admin
from ..utils.info import extract_user_data_from_update
from ...default_handlers.check_subscription.handlers import check_subscription_channel_always
from ...models import User


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )


def help(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)
    update.message.reply_text(text + static_text.help_message, parse_mode='HTML',
                              reply_markup=make_keyboard_for_help_command())


@check_subscription_channel_always
def about(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    if u.is_admin:
        text = static_text.start_not_created.format(first_name=u.first_name)

        update.message.reply_text(text + static_text.about_message, parse_mode='HTML',
                                  reply_markup=make_keyboard_for_about_command_admin())

    if not u.is_admin:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text + static_text.about_message, parse_mode='HTML',
                              reply_markup=make_keyboard_for_about_command())


def ignore_updates(update: Update, context: CallbackContext) -> None:
    return
