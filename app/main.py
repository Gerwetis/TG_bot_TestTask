import asyncio

# TODO подтягивание неиспользуемих импортов
import os
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, AUTH_KEY, DATABASE_URL
from db import Database
from keyboards import file_type_inline_kb, main_menu_kb, auth_kb
from states import AuthStates, UploadStates
from utils import ensure_user_dir, allowed_file

print("DEBUG AUTH_KEY:", repr(AUTH_KEY))

# Підключення бази та бота

db = Database(DATABASE_URL)
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


# TODO: main_menu_kb и auth_kb - лучше брать из отдельного модуля, у тебя он уже создан (keyboards.py)
# def main_menu_kb():
#     return ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="Обробити файл")],
#             [KeyboardButton(text="Розлогінитись")]
#         ],
#         resize_keyboard=True
#     )
#
#

# def auth_kb():
#     return ReplyKeyboardMarkup(
#         keyboard=[[KeyboardButton(text="Ввести ключ")]],
#         resize_keyboard=True
#     )


# Авторизація

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    if await db.is_authorized(message.from_user.id):
        await message.answer("Ви вже авторизовані!", reply_markup=main_menu_kb())
    else:
        await message.answer("Введіть ключ авторизації", reply_markup=auth_kb())
        await state.set_state(AuthStates.waiting_for_key)


@dp.message(AuthStates.waiting_for_key)
async def key_input(message: Message, state: FSMContext):
    key = message.text.strip()
    if key in AUTH_KEY:
        await db.add_user(message.from_user.id, message.from_user.full_name)
        await db.add_log(message.from_user.id, "Авторизувався")
        await message.answer("Успішно авторизовані!", reply_markup=main_menu_kb())
        await state.clear()
    else:
        await message.answer("Невірний ключ. Спробуйте ще раз.")


#  Меню
@dp.message(lambda m: m.text == "Обробити файл")
# TODO: Нужно убрать state: FSMContext, так как ты его не используешь )
async def handle_file(message: Message, state: FSMContext):
    await message.answer("Виберіть тип файлу", reply_markup=file_type_inline_kb())
    await db.add_log(message.from_user.id, "Натиснув Обробити файл")


@dp.callback_query(lambda c: c.data in ["file_doc", "file_photo"])
async def file_type_chosen(c: CallbackQuery, state: FSMContext):
    file_type = "document" if c.data == "file_doc" else "photo"
    await state.update_data(file_type=file_type)
    await c.message.answer(f"Завантажте {file_type}")
    await state.set_state(UploadStates.waiting_for_file)
    await db.add_log(c.from_user.id, f"Обрав тип файлу: {file_type}")
    await c.answer()


@dp.message(UploadStates.waiting_for_file)
async def file_received(message: Message, state: FSMContext):
    # TODO: Не рабочий вариант )
    # file_obj = None
    # if file_type == "document" and message.document:
    #     file_obj = message.document
    # elif file_type == "photo" and message.photo:
    #     file_obj = message.photo[-1]
    #
    # if not file_obj:
    #     await message.answer("Невірний формат файлу. Спробуйте ще раз.")
    #     return
    # file_name = file_obj.file_name if hasattr(file_obj, "file_name") else f"{file_obj.file_id}.jpg"
    # await file_obj.download(destination=file_path)

    # TODO: рабочий вариант
    data = await state.get_data()
    user_id = message.from_user.id
    file_type = data.get("file_type")
    if message.content_type != file_type:
        await message.answer(text="Невірний тип файлу. Спробуйте ще раз.")
        return
    file = message.document if file_type == "document" else message.photo[-1]
    file_name = file.file_name if file_type == "document" else f'{file.file_id}.jpg'
    if not allowed_file(filename=file_name, file_type=file_type, msg_type=message.content_type):
        await message.answer("Невірний формат. Завантажте інший файл.")
        return
    file_path = ensure_user_dir(tg_id=message.from_user.id, file_name=file_name)
    fs = await bot.get_file(file_id=file.file_id)
    await bot.download_file(file_path=fs.file_path, destination=file_path)

    # TODO: Логирование лучше сделать 1м методом, не 2мя.
    await db.add_file(tg_id=user_id, filename=file_name, path=file_path, file_type=file_type)
    await db.add_log(tg_id=user_id, action=f"Завантажив файл: {file_name}")

    await message.answer(text="Файл успішно завантажено!", reply_markup=main_menu_kb())
    await state.clear()


@dp.message(lambda m: m.text == "Розлогінитись")
async def logout(message: Message):
    await db.delete_user(tg_id=message.from_user.id)
    await db.add_log(tg_id=message.from_user.id, action="Розлогінився")
    await message.answer(text="Ви розлогінені", reply_markup=auth_kb())


# Запуск бота

async def main():
    await db.connect()
    print("Бот стартував...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
