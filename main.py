import logging
from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime, timedelta

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8156906168:AAEkPwK8SLo6_3fdmB-zgT1YP_IQnNpdFzE" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_messages = {} # Память для анти-спама

# 1. ПРИВЕТСТВИЕ НОВЫХ УЧАСТНИКОВ
@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def welcome(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Добро пожаловать, {user.first_name}! Протоколы безопасности активированы.")

# 2. ОСНОВНОЙ ОБРАБОТЧИК (ЦИТАТЫ И АНТИ-СПАМ)
@dp.message_handler(lambda m: m.text)
async def main_handler(message: types.Message):
    text = message.text.lower()
    user_id = message.from_user.id

    # --- БЛОК АНТИ-СПАМА ---
    now = datetime.now()
    if user_id not in user_messages:
        user_messages[user_id] = []
    
    # Очистка старых записей (сообщения старше 10 секунд удаляем из памяти)
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < timedelta(seconds=10)]
    user_messages[user_id].append(now)

    # Если больше 5 сообщений за 10 секунд — мут на 20 минут
    if len(user_messages[user_id]) > 5:
        try:
            # Устанавливаем время разблокировки: текущее время + 20 минут
            until_date = datetime.now() + timedelta(minutes=20)
            await message.chat.restrict(user_id, until_date=until_date)
            return await message.answer(f"Сэр, {message.from_user.first_name} слишком шумит. Объявлен режим тишины на 20 минут.")
        except:
            pass # Если бот не админ, он не сможет ограничить доступ

    # --- БЛОК ЦИТАТ ---
    quotes = {
        "джарвис": "Я вас слушаю, сэр. К вашим услугам.",
        "тони": "Я — Железный человек.",
        "тор": "Я Бог Грома! Подайте мне Таноса!",
        "халк": "Халк крушить!",
        "кэп": "Я могу это делать весь день.",
        "капитан": "Я могу это делать весь день.",
        "наташа": "Я больше не хочу бежать от своего прошлого.",
        "бартон": "Никто не видел, как я промахнулся."
    }

    for name, quote in quotes.items():
        if name in text:
            return await message.reply(f"🛡️ {quote}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
