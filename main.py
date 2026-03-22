import logging
from aiogram import Bot, Dispatcher, types, executor

# Вставь сюда свой токен от BotFather
TOKEN = "8756906168:AAEKFWK8SLeG_3fdWB-zgTiYP_IQnMpdFzE"

# Настройка логирования, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Ответ на команду /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Системы Джарвиса активированы. Добрый день, сэр!")

# Реакция на текст
@dp.message_handler()
async def echo_message(message: types.Message):
    text = message.text.lower()
    
    if "джарвис" in text:
        await message.reply("К вашим услугам, сэр. Чем могу помочь?")
    elif "тони" in text:
        await message.reply("Я здесь, сэр. Мистер Старк просил передать, что он занят в мастерской.")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
