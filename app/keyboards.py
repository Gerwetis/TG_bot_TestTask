from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Основне меню
def main_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Обробити файл")],
            [KeyboardButton("Список завантаженних файлів")],
            [KeyboardButton("Розлогінитись")]
        ],
        resize_keyboard=True
    )
    return kb

# Авторизація
def auth_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("Авторизація")]],
        resize_keyboard=True
    )
    return kb

# Inline кнопки типу файлу
def file_type_inline_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Документ", callback_data="file_doc")],
            [InlineKeyboardButton("Фото", callback_data="file_photo")]
        ]
    )
    return kb

