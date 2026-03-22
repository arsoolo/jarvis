import logging
from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime, timedelta

# 1. ЗАГРУЗКА ДАННЫХ
TOKEN = "8156906168:AAEkPwK8SLo6_3fdmB-zgT1YP_IQnNpdFzE" 
BAD_WORDS = ['сука', 'блять', 'хуй', 'пидор', 'еблан', 'уебок']
user_messages = {} 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(lambda m: m.text)
async def main_logic(message: types.Message):
    text = message.text.lower()
    user_id = message.from_user.id

    # --- АНТИ-СПАМ ---
    now = datetime.now()
    if user_id not in user_messages: user_messages[user_id] = []
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < timedelta(seconds=10)]
    user_messages[user_id].append(now)
    if len(user_messages[user_id]) > 5:
        try:
            await message.chat.restrict(user_id, until_date=timedelta(minutes=5))
            return await message.answer("Сэр, слишком много шума. Режим тишины на 5 минут.")
        except: pass

    # --- ОТКЛИК НА ИМЯ ДЖАРВИС ---
    if any(x in text.upper() for x in ["ДЖАРВИС", "Д.Ж.А.Р.В.И.С"]):
        return await message.reply("Я вас слушаю, сэр. К вашим услугам.")

    # --- КОМАНДЫ МУТА/РАЗМУТА ---
    if text.startswith('!мут') or text.startswith('!размут'):
        user_status = await message.chat.get_member(user_id)
        if user_status.is_chat_admin() or user_status.is_chat_creator():
            if not message.reply_to_message:
                return await message.reply("Сэр, укажите цель (ответьте на сообщение).")
            can_send = True if '!размут' in text else False
            try:
                await message.chat.restrict(message.reply_to_message.from_user.id, 
                    permissions=types.ChatPermissions(can_send_messages=can_send, can_send_media_messages=can_send, can_send_other_messages=can_send))
                await message.reply("Протокол выполнен.")
            except:
                await message.reply("Недостаточно прав администратора.")
        return

    # --- ЦИТАТЫ ГЕРОЕВ ---
    hero_quotes = {"тор": "Я Бог Грома!", "халк": "Халк крушить!", "тони": "Я — Железный человек.", "кэп": "Я могу это делать весь день."}
    for hero, quote in hero_quotes.items():
        if hero in text:
            return await message.reply(f"🛡️ {quote}")

    # --- КЭП И МАТЫ ---
    if any(word in text for word in BAD_WORDS):
        user_status = await message.chat.get_member(user_id)
        if not (user_status.is_chat_admin() or user_status.is_chat_creator()):
            await message.reply("⚠️ Капитан Америка: «Не выражаться!» 🛡️")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
