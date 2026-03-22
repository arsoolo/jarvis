import logging
from aiogram import Bot, Dispatcher, types, executor

TOKEN = "8756906168:AAEKFWK8SLeG_3fdWB-zgTiYP_IQnMpdFzE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Системы Джарвиса активированы, сэр!")

@dp.message_handler()
async def echo(message: types.Message):
    if "джарвис" in message.text.lower():
        await message.reply("К вашим услугам, сэр.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
