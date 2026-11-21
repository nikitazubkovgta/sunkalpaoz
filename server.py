import asyncio
import os
import re
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

WELCOME = (
    "Здравствуйте! ✨\n\n"
    "Это бот SUNKALPA — наша обратная связь.\n\n"
    "Расскажите, что вы думаете: поделитесь отзывом, пожеланием или идеей. "
    "Нам важно каждое слово, мы читаем всё лично и обязательно ответим.\n\n"
    "Просто напишите сообщение ниже 👇"
)

THANKS = "Спасибо! Ваше сообщение получено, скоро мы вам ответим 🤍"

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(WELCOME)


@dp.message(F.from_user.id == ADMIN_ID, F.reply_to_message)
async def admin_reply(message: Message):
    original = message.reply_to_message.text or ""
    match = re.search(r"ID: (\d+)", original)
    if not match:
        await message.answer("Не нашёл ID пользователя. Отвечай именно на уведомление о сообщении.")
        return
    user_id = int(match.group(1))
    try:
        await bot.send_message(user_id, message.text)
        await message.answer("✅ Ответ отправлен")
    except Exception as e:
        await message.answer(f"Не удалось отправить: {e}")


@dp.message(F.text, F.from_user.id != ADMIN_ID)
async def user_message(message: Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"
    notice = (
        f"📩 Новое сообщение\n"
        f"От: {user.full_name} ({username})\n"
        f"ID: {user.id}\n\n"
        f"{message.text}"
    )
    await bot.send_message(ADMIN_ID, notice)
    await message.answer(THANKS)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
