from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


# Основне меню
def main_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Обробити файл")],
            [KeyboardButton(text="Список завантаженних файлів")],
            [KeyboardButton(text="Розлогінитись")]
        ],
        resize_keyboard=True
    )
    return kb


# Авторизація
def auth_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Авторизація")]],
        resize_keyboard=True
    )
    return kb


# Inline кнопки типу файлу
def file_type_inline_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            # Fix bug, when can't load KB
            [InlineKeyboardButton(text="Документ", callback_data="file_doc")],
            [InlineKeyboardButton(text="Фото", callback_data="file_photo")]
        ]
    )
    return kb
