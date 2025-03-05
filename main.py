import os
import asyncio
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

load_dotenv()

API_ID = 27620089
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = 5061909214

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

channels = {
    -1001337701474: -1001956847541,
    -1002460046152: -1001694845676,
    -1001980053407: -1002030769789,
    -1001773705589: -1001981481442,
    -1002339069316: -1002212791539,
}


def send_to_bot(message):
    """Bot orqali loglarni yuborish"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"⚠️ Xatolik botga xabar yuborishda: {e}")


async def main():
    await client.start()
    print("✅ Userbot Railway'da ishga tushdi!")
    send_to_bot("✅ Userbot Railway'da ishga tushdi!")


@client.on(events.NewMessage(chats=list(channels.keys())))
async def handler(event):
    try:
        await asyncio.sleep(1)

        if event.is_channel:
            channel_id = event.chat_id
            linked_chat_id = channels.get(channel_id)

            message = f"✅ Yangi post topildi! Kanal ID: {channel_id}, Post ID: {event.id}"
            print(message)
            send_to_bot(message)

            start_time = asyncio.get_event_loop().time()
            found = False

            while asyncio.get_event_loop().time() - start_time < 3:
                async for msg in client.iter_messages(linked_chat_id, limit=10):
                    if msg.forward and msg.forward.original_fwd:
                        if msg.forward.original_fwd.channel_post == event.id:
                            message = f"🔗 Ulangan post topildi! Guruhdagi ID: {msg.id}"
                            print(message)
                            send_to_bot(message)

                            import random
                            comments = [
                                "Ramazon muborak, do'stlar! 🌙",
                                "Alloh ibodatlaringizni qabul qilsin! 🤲",
                                "Bugun ham duolarimizda bir-birimizni eslaylik! 💖",
                                "Zikr va salovat aytish esdan chiqmasin! 🕌",
                            ]
                            comment = random.choice(comments)
                            await client.send_message(linked_chat_id, comment, reply_to=msg.id)

                            message = "💬 Fikr bildirish bo‘limiga sharh yuborildi!"
                            print(message)
                            send_to_bot(message)

                            found = True
                            break

                if found:
                    break

                await asyncio.sleep(0.3)

            if not found:
                message = "⛔ Guruhda mos post topilmadi!"
                print(message)
                send_to_bot(message)

    except Exception as e:
        message = f"⚠️ Xatolik: {e}"
        print(message)
        send_to_bot(message)


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()