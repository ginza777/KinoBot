from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

from ..main_bot.bot import Bot_settings


def make_movie_share_keyboard_with_code(bot_username,code,lang) -> InlineKeyboardMarkup:
    share_bot = {
        "uz": f"Ushbu kinoni ulashing  📤 ",
        "ru": f"Поделиться этим фильмом  📤",
        "en": f"Share this Movie 📤"
    }
    buttons = [[
        InlineKeyboardButton(share_bot[lang], switch_inline_query=f"https://t.me/{bot_username}?start={code}")
    ]]
    return InlineKeyboardMarkup(buttons)

def share_post_inline_button(post_id,lang) -> InlineKeyboardMarkup:
    share_text = {
        "uz": f"Ushbu postni ulashing 📤",
        "ru": f"Поделиться этим постом 📤",
        "en": f"Share this post 📤"
    }
    buttons = [[
        InlineKeyboardButton(share_text[lang], switch_inline_query=f"share_post_{post_id}")
    ]]
    return InlineKeyboardMarkup(buttons)



def start_with_code_keyboard(bot_username,code,lang) -> InlineKeyboardMarkup:
    share_bot = {
        "uz": f"Ushbu kinoni ulashing  📤 ",
        "ru": f"Поделиться этим фильмом  📤",
        "en": f"Share this Movie 📤"
    }
    buttons = [[
        InlineKeyboardButton(share_bot[lang], switch_inline_query=f"https://t.me/{bot_username}?start={code}")
    ]]
    return InlineKeyboardMarkup(buttons)


def make_movie_share_keyboard(lang) -> InlineKeyboardMarkup:
    share_bot = {
        "uz": f"Ushbu kinoni ulashing  📤 ",
        "ru": f"Поделиться этим фильмом  📤",
        "en": f"Share this Movie 📤"
    }
    text = """🍀Full Hd ,4k kinolar 🎥\n🍀Saralangan top dagi kinolar🍿\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Barcha kinolar saralangan ,trenddagi kinolar\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Botni do'stlaringiz bilan ulashing\n🍀Bot uchun havola :@uzbek_kino_time_bot\n🍀Kanalimiz : @uzbek_kino_time\n"""
    buttons = [[
        InlineKeyboardButton(share_bot[lang], switch_inline_query=f"\n\n{text}")
    ]]
    return InlineKeyboardMarkup(buttons)

def movie_share_keyboard(lang) -> InlineKeyboardMarkup:
    share_bot = {
        "uz": f"Ushbu kinoni ulashing  📤 ",
        "ru": f"Поделиться этим фильмом  📤",
        "en": f"Share this Movie 📤"
    }
    text = """🍀Full Hd ,4k kinolar 🎥\n🍀Saralangan top dagi kinolar🍿\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Barcha kinolar saralangan ,trenddagi kinolar\n🍀Kino kodini yuboring va kinoni yuklab oling\n🍀Botni do'stlaringiz bilan ulashing\n🍀Bot uchun havola :@uzbek_kino_time_bot\n🍀Kanalimiz : @uzbek_kino_time\n"""
    buttons = [[
        InlineKeyboardButton(share_bot[lang], switch_inline_query=f"\n\n{text}")
    ]]
    return InlineKeyboardMarkup(buttons)


def default_keyboard(lang) -> ReplyKeyboardMarkup:
    random_movies={
        "uz": "🎲 Random Kino",
        "ru": "🎲 Случайный фильм",
        "en": "🎲 Random Movie"
    }
    top_1_movies={
        "uz": "🎥 Top 1 Kino",
        "ru": "🎥 Top 1 фильмов",
        "en": "🎥 Top 1 Movies"
    }
    top_3_movies={
        "uz": "🎥 Top 3 Kinolar",
        "ru": "🎥 Top 3 Фильмы",
        "en": "🎥 Top 3 Movies"
    }
    change_language={
        "uz": "🌍 Tilni o'zgartirish",
        "ru": "🌍 Изменить язык",
        "en": "🌍 Change Language"
    }
    help={
        "uz": "📚 Yordam",
        "ru": "📚 Помощь",
        "en": "📚 Help"
    }
    share_bot={
        "uz": "📤 Botni ulashish",
        "ru": "📤 Поделиться ботом",
        "en": "📤 Share Bot"
    }

    about_us={
        "uz": "📞 Biz haqimizda",
        "ru": "📞 O_HAC",
        "en": "📞 About Us"
    }

    buttons = [
        [ KeyboardButton(random_movies[lang])],
        # Top 3 movies
        [KeyboardButton(top_1_movies[lang]), KeyboardButton(top_3_movies[lang])],
        # Random movie
        [KeyboardButton(change_language[lang]), KeyboardButton(help[lang])],
        # Share the bot
        [KeyboardButton(share_bot[lang]), KeyboardButton(about_us[lang])]

    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
