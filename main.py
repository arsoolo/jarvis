import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime, timedelta

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8156906168:AAEkPwK8SLo6_3fdmB-zgT1YP_IQnNpdFzE" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_messages = {}

# ПРИВЕТСТВИЕ
@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def welcome(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Добро пожаловать, {user.first_name}!")

# ГЕРОИ И АНТИ-СПАМ
@dp.message_handler(lambda m: m.text)
async def main_handler(message: types.Message):
    text = message.text.lower()
    user_id = message.from_user.id

    # Анти-спам (20 минут мут)
    now = datetime.now()
    if user_id not in user_messages: user_messages[user_id] = []
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < timedelta(seconds=10)]
    user_messages[user_id].append(now)
    if len(user_messages[user_id]) > 5:
        try:
            await message.chat.restrict(user_id, until_date=datetime.now() + timedelta(minutes=20))
            return await message.answer("Сэр, режим тишины на 20 минут за спам.")
        except: pass

    # Цитаты
    quotes = {
        "джарвис": "Я вас слушаю, сэр. К вашим услугам.",
        "тони": "Я — Железный человек.",
        "тор": "Я Бог Грома!",
        "халк": "Халк крушить!",
        "кэп": "Я могу это делать весь день."
    }
    for name, quote in quotes.items():
        if name in text:
            return await message.reply(f"🛡️ {quote}")

if __name__ == '__main__':
    # Эта строчка не даст Render убить процесс
    executor.start_polling(dp, skip_updates=True)
