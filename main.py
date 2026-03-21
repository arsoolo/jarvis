import asyncio
import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F

# Твой токен
TOKEN = "8756906168:AAEKFWK8SLeG_3fdWB-zgTiYP_IQnMpdFzE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

warns = {}
spam_check = {}

# Цитаты героев
MARVEL_QUOTES = {
    "старк": ["Я — Железный человек.", "Дайте мне чизбургер.", "Гений, миллиардер, плейбой, филантроп."],
    "тони": ["Я — Железный человек.", "У нас есть Халк!"],
    "кэп": ["Я могу это делать весь день.", "Мстители, общий сбор!"],
    "тор": ["Принесите мне Таноса!", "Я еще достоин!"],
    "халк": ["Халк крушить!", "Мелковат бог..."],
    "грут": ["Я есть Грут.", "Мы есть Грут."],
    "паук": ["С большой силой приходит большая ответственность."],
}

# Список матов для Капитана Америки
CAPTAIN_WORDS = ["нищий", "тупой", "еблан", "сучка", "пидр", "пидорас", "хуесос", "хуеглот", "уебок", "уебище"]

@dp.message(F.new_chat_members)
async def welcome(message: types.Message):
    for user in message.new_chat_members:
        await message.answer(f"Приветствую, {user.first_name}! 🛡️\nЯ Джарвис. В этом чате живут герои.")

@dp.message(F.text | F.sticker)
async def main_monitor(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    if not (message.text or message.sticker): return
    content = message.text.lower() if message.text else message.sticker.file_unique_id

    # 1. СПАМ
    if user_id not in spam_check:
        spam_check[user_id] = {"content": content, "count": 1}
    else:
        if spam_check[user_id]["content"] == content:
            spam_check[user_id]["count"] += 1
        else:
            spam_check[user_id] = {"content": content, "count": 1}

    if spam_check[user_id]["count"] > 5:
        spam_check[user_id]["count"] = 0
        warns[user_id] = warns.get(user_id, 0) + 1
        until = datetime.now() + timedelta(minutes=30)
        try:
            await bot.restrict_chat_member(message.chat.id, user_id, permissions=types.ChatPermissions(can_send_messages=False), until_date=until)
            await message.answer(f"🚫 {user_name}, мут 30 мин за спам! Варн [{warns[user_id]}/3]")
        except: pass
        return

    # 2. ГЕРОИ
    if message.text:
        for hero, quotes in MARVEL_QUOTES.items():
            if hero in content:
                await message.reply(f"🤖 Джарвис: «{random.choice(quotes)}»")
                return

        # 3. МАТЫ
        if any(word in content for word in CAPTAIN_WORDS):
            warns[user_id] = warns.get(user_id, 0) + 1
            await message.reply(f"⚠️ Капитан Америка: «Не выражаться!» 🛡️\nВарн для {user_name}: [{warns[user_id]}/3]")
            if warns[user_id] >= 3:
                try:
                    await bot.ban_chat_member(message.chat.id, user_id)
                    await message.answer(f"🚀 {user_name} забанен!")
                except: pass

async def main():
    print("--- ДЖАРВИС ОНЛАЙН ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
