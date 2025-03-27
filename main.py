import os
import asyncio
import aiohttp
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import random

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

channels = {
    -1001337701474: ["Zo'r", "Ha", "Uzmobile effekt"],  # Inline
    -1002460046152: ["Ha", "Zo'r", "...", "Uzmobile effekt"],  # Futbolishee
    -1002339069316: ["Zo'r", "Ha", "Uzmobile effekt"],  # cyrax
    -1002331884910: ["Zo'r", "Ha", "Uzmobile effekt", "Efuzpage nomr 1"],  # efuzpage
    -1001974475685: ["Uzmobile effekt", "Ha", "Zo'r"]  # efootball
}


async def send_to_bot(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            if resp.status != 200:
                print(f"⚠️ Botga xabar yuborishda xatolik: {resp.status}")


@client.on(events.NewMessage(chats=list(channels.keys())))
async def handler(event):
    try:
        if event.is_channel:
            channel_id = event.chat_id
            entity = await client.get_entity(channel_id)
            channel_name = entity.title

            comment = random.choice(channels.get(channel_id, ["Ajoyib kanal ekan! 😊"]))
            await client.send_message(channel_id, comment, reply_to=post_id)

            log_message = f"✅ Yangi post topildi! Kanal: {channel_name} (ID: {channel_id}), Post ID: {event.id}\n💬 Sharh yozildi: {comment}"
            print(log_message)
            await send_to_bot(log_message)

    except Exception as e:
        error_message = f"⚠️ Xatolik: {e}"
        print(error_message)
        await send_to_bot(error_message)


@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    try:
        if event.is_private:
            welcome_message = "Assalomu alaykum! Men dasturchilar tomonidan avtomatlashtirilgan userbotman."
            await event.reply(welcome_message)

            log_message = f"💬 Foydalanuvchiga javob yuborildi: {welcome_message}"
            print(log_message)
            await send_to_bot(log_message)

    except Exception as e:
        error_message = f"⚠️ Xatolik (private-reply): {e}"
        print(error_message)
        await send_to_bot(error_message)


async def main():
    await client.start()
    start_message = "✅ Userbot Railway'da ishga tushdi!"
    print(start_message)
    await send_to_bot(start_message)


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
