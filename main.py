import logging
from aiogram import Bot, Dispatcher, types, executor

TOKEN = "8156906168:AAEkPwK8SLo6_3fdmB-zgT1YP_IQnNpdFzE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def test(message: types.Message):
    await message.reply("Сэр, я в сети! Системы активны.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
