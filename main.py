import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загружаем токен и кошелёк из Secrets (в Replit)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

if not BOT_TOKEN or not WALLET_ADDRESS:
    logging.error("❌ BOT_TOKEN или WALLET_ADDRESS не заданы в Secrets!")
    exit(1)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Простое временное хранилище (для MVP)
temp_data = {}

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Получить username", callback_data="get_username")],
        [InlineKeyboardButton(text="💰 Мои лоты", callback_data="my_listings")],
        [InlineKeyboardButton(text="🛒 Каталог", callback_data="catalog")]
    ])
    await message.answer(
        "👋 Добро пожаловать в Маркетплейс Username’ов!\n\n"
        "Получи уникальный username через @fragment → выставь на продажу → заработай TON!",
        reply_markup=keyboard
    )

# Получение username (временно — заглушка)
@dp.callback_query(lambda c: c.data == "get_username")
async def get_username(callback_query: types.CallbackQuery):
    fake_username = "x7kq"  # Позже заменим на реальный из @fragment
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Выставить на продажу", callback_data=f"list_{fake_username}")]
    ])
    await callback_query.message.answer(
        f"🎉 Тебе достался username: @{fake_username}\n\n"
        f"Хочешь выставить его на продажу?",
        reply_markup=keyboard
    )

# Начало выставления на продажу
@dp.callback_query(lambda c: c.data.startswith("list_"))
async def list_username(callback_query: types.CallbackQuery):
    username = callback_query.data.split("_")[1]
    await callback_query.message.answer(f"💰 Введи цену для @{username} в TON (например, 0.5):")
    temp_data[callback_query.from_user.id] = {'username': username}

# Установка цены
@dp.message(lambda message: message.from_user.id in temp_data)
async def set_price(message: types.Message):
    try:
        price = float(message.text)
        if price <= 0:
            raise ValueError
        user_data = temp_data.pop(message.from_user.id)
        username = user_data['username']
        # Пока просто подтверждаем — позже добавим базу данных
        await message.answer(f"✅ @{username} выставлен на продажу за {price} TON! (временно без сохранения)")
    except ValueError:
        await message.answer("❌ Введи корректное положительное число (например, 0.5)")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
