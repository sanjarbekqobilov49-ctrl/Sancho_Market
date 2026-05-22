import asyncio
from django.conf import settings
from telegram import Bot


def send_telegram_message(text):
    if not settings.BOT_TOKEN or not settings.CHAT_ID:
        return
    async def send():
        bot = Bot(token=settings.BOT_TOKEN)
        await bot.send_message(chat_id=settings.CHAT_ID, text=text)
    asyncio.run(send())
