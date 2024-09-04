from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

from ..main_bot.bot import Bot_settings


def make_movie_share_keyboard_with_code(bot_username,code) -> InlineKeyboardMarkup:
    share_bot = f"Share this Movie "
    buttons = [[
        InlineKeyboardButton(share_bot, switch_inline_query=f"https://t.me/{bot_username}?start={code}")
    ]]
    return InlineKeyboardMarkup(buttons)

def share_post_inline_button(post_id) -> InlineKeyboardMarkup:
    share_text = "Share this post"
    buttons = [[
        InlineKeyboardButton(share_text, switch_inline_query=f"share_post_{post_id}")
    ]]
    return InlineKeyboardMarkup(buttons)



def start_with_code_keyboard(bot_username,code) -> InlineKeyboardMarkup:
    share_bot = f"Share this Movie "
    buttons = [[
        InlineKeyboardButton(share_bot, switch_inline_query=f"https://t.me/{bot_username}?start={code}")
    ]]
    return InlineKeyboardMarkup(buttons)


def make_movie_share_keyboard() -> InlineKeyboardMarkup:
    share_bot = f"Share this Movie "
    text = """🍀Full Hd ,4k kinolar 🎥\n🍀Saralangan top dagi kinolar🍿\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Barcha kinolar saralangan ,trenddagi kinolar\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Botni do'stlaringiz bilan ulashing\n🍀Bot uchun havola :@uzbek_kino_time_bot\n🍀Kanalimiz : @uzbek_kino_time\n"""
    buttons = [[
        InlineKeyboardButton(share_bot, switch_inline_query=f"\n\n{text}")
    ]]
    return InlineKeyboardMarkup(buttons)

def movie_share_keyboard() -> InlineKeyboardMarkup:
    share_bot = f"Share this Bot "
    text = """🍀Full Hd ,4k kinolar 🎥\n🍀Saralangan top dagi kinolar🍿\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Barcha kinolar saralangan ,trenddagi kinolar\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Botni do'stlaringiz bilan ulashing\n🍀Bot uchun havola :@uzbek_kino_time_bot\n🍀Kanalimiz : @uzbek_kino_time\n"""
    buttons = [[
        InlineKeyboardButton(share_bot, switch_inline_query=f"\n\n{text}")
    ]]
    return InlineKeyboardMarkup(buttons)


def default_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        # [KeyboardButton("🔍 Search Movies"), KeyboardButton("🎲 Random Movie")],
        # Top 3 movies
        [KeyboardButton("🎥 Top 1 Movies"), KeyboardButton("🎥 Top 3 Movies")],
        # Random movie
        [KeyboardButton("🌍 Change Language"), KeyboardButton("📚 Help")],
        # Share the bot
        [KeyboardButton("📤 Share Bot"), KeyboardButton("📞 About Us")]

    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
