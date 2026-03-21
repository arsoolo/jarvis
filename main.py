import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime, timedelta

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8756906168:AAEKFWK8SLeG_3fdWB-zgTiYP_IQnMpdFzE" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# БАЗЫ ДАННЫХ
BAD_WORDS = ['сука', 'блять', 'хуй', 'пидор', 'еблан', 'уебок']
user_messages = {} # Для анти-спама

# 1. ПРИВЕТСТВИЕ
@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def welcome(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Добро пожаловать в Башню Мстителей, {user.first_name}! Протоколы безопасности активированы.")

# 2. ОТКЛИК НА ИМЯ ДЖАРВИС
@dp.message_handler(lambda m: m.text and any(x in m.text.upper() for x in ["ДЖАРВИС", "Д.Ж.А.Р.В.И.С"]))
async def jarvis_call(message: types.Message):
    import random
    responses = ["Я вас слушаю, сэр.", "К вашим услугам, сэр.", "Все системы функционируют нормально."]
    await message.reply(random.choice(responses))

# 3. ОСНОВНОЙ ОБРАБОТЧИК (АНТИ-СПАМ, ГЕРОИ, КЭП)
@dp.message_handler(lambda m: m.text)
async def main_logic(message: types.Message):
    text = message.text.lower()
    user_id = message.from_user.id

    # --- АНТИ-СПАМ ---
    now = datetime.now()
    if user_id not in user_messages:
        user_messages[user_id] = []
    # Очищаем старые сообщения (старше 10 сек)
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < timedelta(seconds=10)]
    user_messages[user_id].append(now)

    if len(user_messages[user_id]) > 5:
        try:
            await message.chat.restrict(user_id, until_date=timedelta(minutes=5))
            return await message.answer(f"Сэр, {message.from_user.first_name} слишком шумит. Мут на 5 минут за спам.")
        except: pass

    # --- КОМАНДЫ МУТА/РАЗМУТА ---
    if text.startswith('!мут') or text.startswith('!размут'):
        user_status = await message.chat.get_member(user_id)
        if user_status.is_chat_admin() or user_status.is_chat_creator():
            if not message.reply_to_message:
                return await message.reply("Сэр, ответьте на сообщение цели.")
            
            # Если команда !размут — разрешаем всё, если !мут — запрещаем
            can_send = True if '!размут' in text else False
            try:
                await message.chat.restrict(message.reply_to_message.from_user.id, 
                    permissions=types.ChatPermissions(
                        can_send_messages=can_send, 
                        can_send_media_messages=can_send, 
                        can_send_other_messages=can_send,
                        can_add_web_page_previews=can_send
                    ))
                await message.reply("Протокол выполнен. Статус цели изменен.")
            except:
                await message.reply("Ошибка: проверьте мои права администратора.")
        return

    # --- ЦИТАТЫ ПЕРСОНАЖЕЙ ---
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
            return # Чтобы не срабатывал Кэп, если в фразе есть и имя, и мат

    # --- КЭП И МАТЫ (БЕЗ ВАРНОВ) ---
    if any(word in text for word in BAD_WORDS):
        user_status = await message.chat.get_member(user_id)
        if not (user_status.is_chat_admin() or user_status.is_chat_creator()):
            await message.reply("⚠️ Капитан Америка: «Не выражаться!» 🛡️")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
