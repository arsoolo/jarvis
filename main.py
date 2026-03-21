import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime, timedelta

# --- ПРОТОКОЛ ДОСТУПА ---
TOKEN = "8756906168:AAEKFWK8SLeG_3fdWB-zgTiYP_IQnMpdFzE" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- БАЗА ДАННЫХ ---
BAD_WORDS = ['сука', 'блять', 'хуй', 'пидор', 'еблан', 'уебок']
user_messages = {} # Для анти-спама

# --- ПРИВЕТСТВИЕ ПРИ ВХОДЕ ---
@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def welcome(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Добро пожаловать в Башню Мстителей, {user.first_name}! Протоколы безопасности активированы.")

# --- ОТКЛИК НА ИМЯ ДЖАРВИС ---
@dp.message_handler(lambda m: any(x in m.text.upper() for x in ["ДЖАРВИС", "Д.Ж.А.Р.В.И.С"]))
async def jarvis_call(message: types.Message):
    import random
    responses = ["Я вас слушаю, сэр.", "К вашим услугам, сэр.", "Все системы функционируют нормально, сэр."]
    await message.reply(random.choice(responses))

# --- ЦИТАТЫ ГЕРОЕВ ---
@dp.message_handler(lambda m: m.text)
async def main_logic(message: types.Message):
    text = message.text.lower()
    user_id = message.from_user.id

    # 1. АНТИ-СПАМ (5 сообщений за 10 секунд)
    now = datetime.now()
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id] = [msg_time for msg_time in user_messages[user_id] if now - msg_time < timedelta(seconds=10)]
    user_messages[user_id].append(now)

    if len(user_messages[user_id]) > 5:
        try:
            await message.chat.restrict(user_id, until_date=timedelta(minutes=5))
            return await message.answer(f"Сэр, {message.from_user.first_name} слишком много шумит. Ограничил доступ на 5 минут.")
        except: pass

    # 2. МУТ / РАЗМУТ (Команды для админов)
    if text.startswith('!мут') or text.startswith('/mute'):
        user_status = await message.chat.get_member(user_id)
        if user_status.is_chat_admin() or user_status.is_chat_creator():
            if not message.reply_to_message:
                return await message.reply("Сэр, ответьте на сообщение цели.")
            await message.chat.restrict(message.reply_to_message.from_user.id, permissions=types.ChatPermissions(can_send_messages=False))
            await message.reply("Цель обезврежена. Режим молчания активирован.")
        return

    if text.startswith('!размут') or text.startswith('/unmute'):
        user_status = await message.chat.get_member(user_id)
        if user_status.is_chat_admin() or user_status.is_chat_creator():
            if not message.reply_to_message:
                return await message.reply("Сэр, укажите кого вернуть в строй.")
            await message.chat.restrict(message.reply_to_message.from_user.id, permissions=types.ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            await message.reply("Ограничения сняты. С возвращением!")
        return

    # 3. ПЕРСОНАЖИ
    hero_quotes = {
        "тор": "Я Бог Грома! Подайте мне Таноса!",
        "халк": "Халк крушить!",
        "наташа": "Я больше не хочу бежать от своего прошлого.",
        "бартон": "Никто не видел, как я промахнулся.",
        "кэп": "Я могу это делать весь день.",
        "капитан": "Я могу это делать весь день.",
        "тони": "Я — Железный человек."
    }
    
    for hero, quote in hero_quotes.items():
        if hero in text:
            await message.answer(f"🛡️ {quote}")

    # 4. КЭП И МАТЫ
    if any(word in text for word in BAD_WORDS):
        user_status = await message.chat.get_member(user_id)
        if not (user_status.is_chat_admin() or user_status.is_chat_creator()):
            await message.reply("⚠️ Капитан Америка: «Не выражаться!» 🛡️")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
