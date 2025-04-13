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
    # -1001337701474: ["Zo'r", "Ha", "Мхм\n\nРаетса\nХихихи\nРаетса\nРаетса\nЧо\nхадоди\n\n😂"],  # Inline
    # -1002460046152: ["Ha", "Zo'r", "...", "suv kabi bo'l", "Мхм\n\nРаетса\nХихихи\nРаетса\nРаетса\nЧо\nхадоди\n\n😂"],
    # Futbolishee
    -1002421347022: ["Zo'r", "Ha"],  # bekorchi
    # -1002331884910: ["Zo'r", "Ha", "Uzmobile effekt", "Efuzpage nomr 1",
    #                  "Мхм\n\nРаетса\nХихихи\nРаетса\nРаетса\nЧо\nхадоди\n\n😂"],  # efuzpage
    # -1001974475685: ["Uzmobile effekt", "Ha", "Zo'r", "Мхм\n\nРаетса\nХихихи\nРаетса\nРаетса\nЧо\nхадоди\n\n😂"],
    # efootball
    # -1001449117896: ["ha", "Мхм\n\nРаетса\nХихихи\nРаетса\nРаетса\nЧо\nхадоди\n\n😂"],  # Stock
    -1001666463882: ["ha", "eng zo'r kanal"]  # private cr7
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
        channel_id = event.chat_id
        entity = await client.get_entity(channel_id)
        channel_name = entity.title

        comment = random.choice(channels[channel_id])

        await client.send_message(
            entity=channel_id,
            message=comment,
            comment_to=event.id
        )
        clean_channel_id = str(channel_id).replace("-100", "")

        channel_link = f"https://t.me/c/{clean_channel_id}"

        log_message = f"✅ Yangi post topildi!\nKanal: {channel_name}: {channel_link}\nID: {channel_id},\nPost ID: {event.id}\n💬 Sharh yozildi: {comment}"
        print(log_message)
        await send_to_bot(f"Bekorchi: {log_message}")

    except Exception as e:
        error_message = f"⚠️ Xatolik: {e}"
        print(error_message)
        await send_to_bot(f"Bekorchi: {error_message}")


@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    try:
        if event.is_private:
            welcome_message = "Assalomu alaykum! Men dasturchilar tomonidan avtomatlashtirilgan userbotman."
            await event.reply(welcome_message)

            log_message = f"💬 Foydalanuvchiga javob yuborildi: {welcome_message}"
            print(log_message)
            await send_to_bot(f"Bekorchi: {log_message}")

    except Exception as e:
        error_message = f"⚠️ Xatolik (private-reply): {e}"
        print(error_message)
        await send_to_bot(f"Bekorchi: {error_message}")


async def main():
    await client.start()
    start_message = "✅ Userbot ishga tushdi!"
    print(start_message)
    await send_to_bot(start_message)


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
