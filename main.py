import os
import asyncio
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import json

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("API_ID:", API_ID)
print("API_HASH:", API_HASH)

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

channels = {
    -1001337701474: -1001956847541,
    -1002460046152: -1001694845676,
    -1001980053407: -1002030769789,
    -1001773705589: -1001981481442,
    -1002339069316: -1002212791539,
    -1002331884910: -1002273035080,
    -1001449117896: -1002409602563
}


def send_to_bot(message):
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
                                "Juda foydali kanal ekan! 👍",
                                "FUTBOL TIME ⚽️\nZinedine Zidane — fransiyalik afsonaviy futbolchi va murabbiy. U 1972 yil 23 iyunda tug‘ilgan. Zidane 1998 yilgi Jahon chempionatida Fransiyani chempionlikka yetaklagan. Klub darajasida Real Madrid va Juventus klublarida o‘ynagan. Murabbiy sifatida Real Madrid bilan uch marta ketma-ket Chempionlar Ligasida g‘olib chiqqan.",
                                "FUTBOL TIME ⚽️\nKevin De Bruyne — belgiyalik professional futbolchi, Manchester City klubi va Belgiya terma jamoasi yarim himoyachisi. U 1991 yil 28 iyunda tug‘ilgan. De Bruyne yarim himoyadagi ajoyib texnikasi va to‘p uzatishlari bilan tanilgan. U bir necha bor Angliya Premyer Ligasining eng yaxshi futbolchilaridan biri deb tan olingan.",
                                "FUTBOL TIME ⚽️\nRobert Lewandowski — polyak professional futbolchi, Barcelona klubi va Polsha terma jamoasi hujumchisi. U 1988 yil 21 avgustda tug‘ilgan. Bayern Munich tarkibida ko‘plab chempionliklarga erishgan va 2020 yilda FIFA tomonidan yilning eng yaxshi futbolchisi deb e’tirof etilgan.",
                                "FUTBOL TIME ⚽️\nHarry Kane — ingliz professional futbolchi, Bayern Munich klubi va Angliya terma jamoasi hujumchisi. U 1993 yil 28 iyulda tug‘ilgan. Kane uzoq yillar Tottenham Hotspur klubida o‘ynagan va Angliya Premyer Ligasining eng yaxshi to‘purarlaridan biri bo‘lgan.",
                                "FUTBOL TIME ⚽️\nModrich va Kroos — zamonaviy futbolning eng kuchli yarim himoyachilari. Luka Modrich Xorvatiya terma jamoasi sardori bo‘lib, 2018 yilgi Jahon chempionatida kumush medal olgan va Oltin to‘p sohibi bo‘lgan. Toni Kroos esa Germaniya bilan 2014 yilgi Jahon chempionatida g‘olib chiqqan.",
                                "FUTBOL TIME ⚽️\nSalah va Mane — Afrikaning eng kuchli futbolchilaridan. Mohamed Salah Liverpool klubining hujumchisi bo‘lib, Chempionlar Ligasi va Premyer Liga g‘olibi. Sadio Mane esa Senegal terma jamoasi yetakchisi bo‘lib, 2022 yilda Afrika Millatlar Kubogida g‘alaba qozongan.",
                                "FUTBOL TIME ⚽️\nVinicius Jr. va Rodrygo — Braziliyaning yosh va iqtidorli futbolchilari. Ikkalasi ham Real Madrid tarkibida Chempionlar Ligasida g‘olib bo‘lgan va kelajak yulduzlari sifatida ko‘rilmoqda.",
                                "FUTBOL TIME ⚽️\nJude Bellingham — ingliz professional futbolchi, Real Madrid klubi va Angliya terma jamoasi yarim himoyachisi. U 2003 yil 29 iyunda tug‘ilgan. Borussia Dortmundda porlagan va 2023 yilda Real Madridga qo‘shilgan. Bellingham Yevropaning eng iqtidorli yosh futbolchilaridan biri hisoblanadi."
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
