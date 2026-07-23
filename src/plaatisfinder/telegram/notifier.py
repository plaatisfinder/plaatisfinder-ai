import os

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()


async def send_message(text: str):
    bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
    await bot.send_message(
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        text=text,
    )