import logging
from aiogram import Bot, Dispatcher, types, executor

# 1. ЗАГРУЗКА ДАННЫХ (САМЫЙ ВЕРХ)
TOKEN = "8756906168:AAEKFWK8SLeG_3fdWB-zgTiYP_IQnMpdFzE"
BAD_WORDS = ['сука', 'блять', 'хуй', 'пидор', 'еблан', 'уебок']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 2. ГЛАВНЫЙ ОБРАБОТЧИК (Python идет сверху вниз)
@dp.message_handler(lambda m: m.text)
async def main_logic(message: types.Message):
    text = message.text.lower()

    # Сначала проверяем: не ДЖАРВИС ли это?
    if any(x in text.upper() for x in ["ДЖАРВИС", "Д.Ж.А.Р.В.И.С"]):
        return await message.reply("Я вас слушаю, сэр. К вашим услугам.")

    # Потом проверяем: не МУТ ли это? (Команды админа)
    if text.startswith('!мут') or text.startswith('!размут'):
        # ... тут код мута ...
        return 

    # Потом проверяем: не ГЕРОИ ли это?
    hero_quotes = {"тор": "Я Бог Грома!", "халк": "Халк крушить!", "тони": "Я — Железный человек."}
    for hero, quote in hero_quotes.items():
        if hero in text:
            return await message.reply(f"🛡️ {quote}")

    # И В САМОМ КОНЦЕ — КЭП (если ничего выше не сработало)
    if any(word in text for word in BAD_WORDS):
        user_status = await message.chat.get_member(message.from_user.id)
        if not (user_status.is_chat_admin() or user_status.is_chat_creator()):
            await message.reply("⚠️ Капитан Америка: «Не выражаться!» 🛡️")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
