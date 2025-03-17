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
    -1001337701474: -1001956847541,  # Inline
    -1002460046152: -1001694845676,  # Futbolishee
    -1002339069316: -1002212791539,  # cyrax
    -1002331884910: -1002273035080,  # Efuzpage
    -1001974475685: -1002106652656  # efootball
}

channel_comments = {
    -1001337701474: ["Zo'r", "Ha", "Uzmobile effekt"],
    -1002460046152: ["Ha", "Zo'r", "...", "Uzmobile effekt"],
    -1002331884910: ["Zo'r", "Ha", "Uzmobile effekt", "Efuzpage nomr 1"],
    -1001974475685: ["Uzmobile effekt", "Ha", "Zo'r"],
    -1002339069316: ["Zo'r", "Ha", "Uzmobile effekt"]
}

auto_replies = ["Haa", "Zo'r", "Nmo'lyapti", "Bilasizmi bazilar meni post kutib o'tiradi deb o'ylarkan"]


async def send_to_bot(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            if resp.status != 200:
                print(f"⚠️ Botga xabar yuborishda xatolik: {resp.status}")


async def main():
    await client.start()
    print("✅ Userbot Railway'da ishga tushdi!")
    await send_to_bot("✅ Userbot Railway'da ishga tushdi!")


@client.on(events.NewMessage(chats=list(channels.keys())))
async def handler(event):
    try:
        if event.is_channel:
            channel_id = event.chat_id
            linked_chat_id = channels.get(channel_id)

            entity = await client.get_entity(channel_id)
            channel_name = entity.title

            message = f"✅ Yangi post topildi! Kanal: {channel_name} (ID: {channel_id}), Post ID: {event.id}"
            print(message)
            await send_to_bot(message)

            messages = await client.get_messages(linked_chat_id, limit=10)

            for msg in messages:
                if msg.forward and msg.forward.original_fwd and msg.forward.original_fwd.channel_post == event.id:
                    comment = random.choice(channel_comments.get(channel_id, ["Ajoyib kanal ekan! 😊"]))

                    await asyncio.gather(
                        client.send_message(linked_chat_id, comment, reply_to=msg.id),
                        send_to_bot(f"💬 Sharh yuborildi!: {comment}")
                    )
                    return

            await send_to_bot("⛔ Guruhda mos post topilmadi!")

    except Exception as e:
        await send_to_bot(f"⚠️ Xatolik: {e}")


@client.on(events.NewMessage(chats=list(channels.values()), incoming=True))
async def auto_reply(event):
    try:
        self_id = (await client.get_me()).id  # Userbot ID

        # Agar xabar kimningdir javobi bo‘lsa
        if event.is_reply and event.reply_to_msg_id:
            original_message = await event.get_reply_message()

            # Agar javob userbot yozgan xabarga bo'lsa
            if original_message and original_message.sender_id == self_id:
                reply_message = random.choice(auto_replies)
                await event.reply(reply_message)
                print(f"🔄 Auto-reply yuborildi: {reply_message}")

    except Exception as e:
        print(f"⚠️ Xatolik (auto-reply): {e}")


@client.on(events.NewMessage(incoming=True))
async def private_reply(event):
    try:
        if event.is_private:
            welcome_message = "Assalomu alaykum! Men dasturchilar tomonidan avtomatlashtirilgan userbotman."
            await event.reply(welcome_message)
            await send_to_bot(f"💬 Foydalanuvchiga javob yuborildi: {welcome_message}")

    except Exception as e:
        print(f"⚠️ Xatolik (private-reply): {e}")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()