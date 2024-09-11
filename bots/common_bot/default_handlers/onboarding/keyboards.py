from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .manage_data import SECRET_LEVEL_BUTTON
from .static_text import github_button_text, secret_level_button_text, admin_button_text
from ...main_bot import bot


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    bot_instance = bot.Bot_settings
    share_bot = f"Share to Friends"
    buttons = [[
        InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}'),
        InlineKeyboardButton(share_bot, switch_inline_query="Share this bot with your friends!")
    ]]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_about_command() -> InlineKeyboardMarkup:
    buttons = [[
        # InlineKeyboardButton(github_button_text, url="https://github.com/GinzaPro/CommonBot.git"),
        # InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}'),
        InlineKeyboardButton(admin_button_text, url="https://t.me/+998336443434")
    ]]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_about_command_admin() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(github_button_text, url="https://github.com/GinzaPro/CommonBot.git"),
        InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}'),
        InlineKeyboardButton(admin_button_text, url="https://t.me/sherzamon_m")
    ]]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_help_command() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(admin_button_text, url="https://t.me/+998336443434")
    ]]

    return InlineKeyboardMarkup(buttons)
