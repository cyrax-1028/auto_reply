import os
import asyncio
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

load_dotenv()

API_ID = 27620089
API_HASH = "5108a02b13715f247a66127db0f178ea"
STRING_SESSION = "1ApWapzMBuz7xGSxxTuYb8D_f6SBS5nDv4ZgPYnku-OsuNzvjIDLixxeUu42DIwhSjaZL5waZFnLTrMKQ97i834oCEf-izrpB-6PcGjsxD6ETPJf_7hIAYUgpQAu8aBtB7Ap-WbNaN5TACpTv7ESEP6QlDEyvzcKjhQb8yQHpBGOMvE4rAVzsuf6QdsIIMmz7olMtWxdHPz0cpHN5UjnaeypM1r-L04Vl2s8i9DaYRmF2udGWHW2jEkKzQhCljwx1BJKXyw0jlY9L6vFLS6HGZ-h0paiWcx_8h9XAIMFhfMzrKiYu3FBqRTq7K_gX-TclM1qTlpmT2qVcctYiq69kpBIw3pnznNY="
BOT_TOKEN = "7530384817:AAHZ_BB4mK_3xm8on-QUFUtUFP3lgEUQ9T0"
CHAT_ID = "5061909214"

print("API_ID:", API_ID)
print("API_HASH:", API_HASH)

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

channels = {
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
        # await asyncio.sleep(1)

        if event.is_channel:
            channel_id = event.chat_id
            linked_chat_id = channels.get(channel_id)

            entity = await client.get_entity(channel_id)
            channel_name = entity.title

            message = f"✅ Yangi post topildi! Kanal: {channel_name} (ID: {channel_id}), Post ID: {event.id}"
            print(message)
            send_to_bot(message)

            start_time = asyncio.get_event_loop().time()
            found = False

            while asyncio.get_event_loop().time() - start_time < 5:
                async for msg in client.iter_messages(linked_chat_id, limit=10):
                    if msg.forward and msg.forward.original_fwd:
                        if msg.forward.original_fwd.channel_post == event.id:
                            message = f"🔗 Ulangan post topildi! Guruhdagi ID: {msg.id}"
                            print(message)
                            send_to_bot(message)

                            import random
                            comments = [
                                 "Kuzatib boryapman yaxshi kanal ekan 👍",
                                "Nechinchi bo'ldim",
"Futboldan zavqlanish kerak asabiylashish kerak emas"
                            ]
                            comment = random.choice(comments)
                            await client.send_message(linked_chat_id, comment, reply_to=msg.id)

                            message = f"💬 Fikr bildirish bo‘limiga sharh yuborildi!: {comment}"
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
