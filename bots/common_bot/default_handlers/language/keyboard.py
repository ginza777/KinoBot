from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def language_list_keyboard():
    button_list = [
        {"name": "🇺🇿 Uzbek", "id": "uz"},
        {"name": "🇬🇧 English", "id": "en"},
        {"name": "🇷🇺 Russian", "id": "ru"},
    ]
    keyboard = []
    for button in button_list:
        keyboard.append([InlineKeyboardButton(button['name'], callback_data=f"language_setting_{button['id']}")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"setting_back")])

    return InlineKeyboardMarkup(keyboard)
