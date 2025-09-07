import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

if not BOT_TOKEN or not WALLET_ADDRESS:
    logging.error("❌ Secrets не заданы!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

# Заглушка под получение username
@dp.callback_query(lambda c: c.data == "get_username")
async def get_username(callback_query: types.CallbackQuery):
    # Позже заменим на реальное взаимодействие с @fragment
    fake_username = "x7kq"  # временно
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Выставить на продажу", callback_data=f"list_{fake_username}")]
    ])
    await callback_query.message.answer(
        f"🎉 Тебе достался username: @{fake_username}\n\n"
        f"Хочешь выставить его на продажу?",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
