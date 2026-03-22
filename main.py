import logging
from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime, timedelta

# ТВОЙ ТОКЕН
TOKEN = "8156906168:AAEkPwK8SLo6_3fdmB-zgT1YP_IQnNpdFzE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
user_messages = {}

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def welcome(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Добро пожаловать, {user.first_name}!")

@dp.message_handler(lambda m: m.text)
async def main_logic(message: types.Message):
    user_id = message.from_user.id
    text = message.text.lower()

    # АНТИ-СПАМ (20 МИН)
    now = datetime.now()
    if user_id not in user_messages: user_messages[user_id] = []
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < timedelta(seconds=10)]
    user_messages[user_id].append(now)
    
    if len(user_messages[user_id]) > 5:
        try:
            await message.chat.restrict(user_id, until_date=datetime.now() + timedelta(minutes=20))
            return await message.answer("Мут 20 минут за спам.")
        except: pass

    # ЦИТАТЫ
    hero_quotes = {
        "джарвис": "Слушаю, сэр.",
        "тони": "Я — Железный человек.",
        "тор": "Я Бог Грома!",
        "кэп": "Не выражаться!"
    }
    for hero, quote in hero_quotes.items():
        if hero in text:
            return await message.reply(quote)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
