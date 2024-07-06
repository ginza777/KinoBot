from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from bots.common_bot.bot import bot_dp
from . import static_text
from ...main_bot.models import Channel


def keyboard_check_subscription_channel():
    channels = Channel.objects.all()
    buttons = []
    for idx, channel in enumerate(channels):
        buttons.append(
            [InlineKeyboardButton(text=f"channel {idx + 1}", url=f"https://t.me/{channel.channel_username}")])

    check_channels_button = InlineKeyboardButton(static_text.check_subscribing, callback_data="check_subscription")
    buttons.append([check_channels_button])

    return InlineKeyboardMarkup(buttons)


def keyboard_checked_subscription_channel(user_id):
    channels = Channel.objects.all()
    buttons = []
    is_subscribed = True

    for idx, channel in enumerate(channels):

        subscribed = not bot_dp.get_chat_member(chat_id=channel.channel_id, user_id=user_id).status == 'left'
        subscription_status = "✅" if subscribed else "❌"
        buttons.append([InlineKeyboardButton(text=f"channel {idx + 1} {subscription_status}",
                                             url=f"https://t.me/{channel.channel_username}")])
        # Update is_subscribed if any channel shows not subscribed
        if not subscribed:
            is_subscribed = False

    check_channels_button = InlineKeyboardButton(static_text.check_subscribing, callback_data="check_subscription")
    buttons.append([check_channels_button])

    return InlineKeyboardMarkup(buttons), is_subscribed


def RemoveKeyboard():
    return ReplyKeyboardRemove()
