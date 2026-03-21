import logging
from aiogram import Bot, Dispatcher, types, executor

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8756906168:AAEKFWK8SLeG_3fdWB-zgTiYP_IQnMpdFzE" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- СПИСОК СЛОВ ---
BAD_WORDS = ['сука', 'блять', 'хуй', 'пидор', 'еблан'] 

# --- КЭП (ТОЛЬКО ТЕКСТ, БЕЗ ВАРНОВ И УДАЛЕНИЯ) ---
@dp.message_handler(lambda m: m.text and any(word in m.text.lower() for word in BAD_WORDS))
async def cap_quote(message: types.Message):
    user_status = await message.chat.get_member(message.from_user.id)
    # Игнорируем админов
    if not (user_status.is_chat_admin() or user_status.is_chat_creator()):
        await message.reply("⚠️ Капитан Америка: «Не выражаться!» 🛡️")

# --- ПРОВЕРКА ---
@dp.message_handler(lambda m: "тони" in m.text.lower())
async def jarvis_status(message: types.Message):
    await message.reply("Я здесь, сэр. Все системы под контролем.")

# --- РАЗМУТ ---
@dp.message_handler(lambda m: m.text and m.text.lower().startswith(('!размут', '/unmute')))
async def system_unmute(message: types.Message):
    user_status = await message.chat.get_member(message.from_user.id)
    if not (user_status.is_chat_admin() or user_status.is_chat_creator()):
        return
    if not message.reply_to_message:
        return await message.reply("Сэр, ответьте на сообщение цели.")
    try:
        await message.chat.restrict(user_id=message.reply_to_message.from_user.id, 
            permissions=types.ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
        await message.reply("Ограничения сняты. Пользователь восстановлен.")
    except:
        await message.reply("Ошибка прав администратора.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
