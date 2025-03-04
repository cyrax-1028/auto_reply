import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

load_dotenv()

API_ID = 27620089
API_HASH = "5108a02b13715f247a66127db0f178ea"
STRING_SESSION = "1ApWapzMBuz7xGSxxTuYb8D_f6SBS5nDv4ZgPYnku-OsuNzvjIDLixxeUu42DIwhSjaZL5waZFnLTrMKQ97i834oCEf-izrpB-6PcGjsxD6ETPJf_7hIAYUgpQAu8aBtB7Ap-WbNaN5TACpTv7ESEP6QlDEyvzcKjhQb8yQHpBGOMvE4rAVzsuf6QdsIIMmz7olMtWxdHPz0cpHN5UjnaeypM1r-L04Vl2s8i9DaYRmF2udGWHW2jEkKzQhCljwx1BJKXyw0jlY9L6vFLS6HGZ-h0paiWcx_8h9XAIMFhfMzrKiYu3FBqRTq7K_gX-TclM1qTlpmT2qVcctYiq69kpBIw3pnznNY="

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

channels = {
    "@REALMADRID_BARSELONA_SPORTTV1": -1001956847541,
    "@FUTBOLISHEEE_FUTBOLISHEEEUZ": -1001694845676,
    "@VAMOSFARRUKH": -1002030769789,
    "@Bilimdon_intelektual_shou": -1001981481442,
    "@cyrax_1028": -1002212791539,
}


async def main():
    await client.start()
    print("✅ Userbot Railway'da ishga tushdi!")


@client.on(events.NewMessage(chats=list(channels.keys())))
async def handler(event):
    try:
        await asyncio.sleep(1)

        if event.is_channel:
            channel_name = event.chat.username
            linked_chat_id = channels.get(f"@{channel_name}")
            print(f"✅ Yangi post topildi! Kanal: @{channel_name}, Post ID: {event.id}")

            start_time = asyncio.get_event_loop().time()
            found = False

            while asyncio.get_event_loop().time() - start_time < 3:
                async for msg in client.iter_messages(linked_chat_id, limit=10):
                    if msg.forward and msg.forward.original_fwd and msg.forward.original_fwd.channel_post == event.id:
                        print(f"🔗 Ulangan post topildi! Guruhdagi ID: {msg.id}")

                        import random

                        comments = [
                            "Ramazon muborak, do'stlar! 🌙",
                            "Alloh ibodatlaringizni qabul qilsin! 🤲",
                            "Bugun ham duolarimizda bir-birimizni eslaylik! 💖",
                            "Zikr va salovat aytish esdan chiqmasin! 🕌",
                        ]

                        comment = random.choice(comments)
                        await client.send_message(linked_chat_id, comment, reply_to=msg.id)

                        print("💬 Fikr bildirish bo‘limiga sharh yuborildi!")
                        found = True
                        break

                if found:
                    break

                await asyncio.sleep(0.3)

            if not found:
                print("⛔ Guruhda mos post topilmadi!")

    except Exception as e:
        print(f"⚠️ Xatolik: {e}")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()