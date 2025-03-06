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

# channels = {
#     -1001337701474: -1001956847541,
#     -1002460046152: -1001694845676,
#     -1001980053407: -1002030769789,
#     -1001773705589: -1001981481442,
#     -1002339069316: -1002212791539,
#     -1002331884910: -1002273035080,
#     -1001449117896: -1002409602563
# }


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
                                "FUTBOL TIME ⚽️\nPele — braziliyalik futbolchi. 3 karra jahon chempioni. 1956-1974-yillarda „Santos“ klubida, 1957-1970-yillarda Braziliya terma jamoasi tarkibida oʻynagan. „Santos“ futbolchilari bilan birga Janubiy Amerika chempionlari kubogi va qitʼalararo kubok egasi.",
                                "Ronaldo 👍\nMessi 🔥\nAntony ❤️",
                                "Kuzatib boryapman yaxshi kanal ekan 👍",
                                "FUTBOL TIME ⚽️\nNeymar braziliyalik professional futbolchi, Al Hilal klubi va Braziliya terma jamoasi hujumchisi. U 1992 yil 5 fevralda tug‘ilgan. Faoliyatini Santos klubida boshlagan, 2013 yilda Barcelona safiga qo‘shilib, Chempionlar Ligasi g‘olibi bo‘lgan. 2017 yilda rekord summa evaziga PSGga o‘tgan va bir necha bor Liga 1 chempioni bo‘lgan. 2023 yilda Al Hilalga transfer qilindi. Braziliya terma jamoasi bilan Konfederatsiyalar kubogi va Olimpiada oltin medalini qo‘lga kiritgan.",
                                "FUTBOL TIME ⚽️\nDiego Maradona argentinalik afsonaviy futbolchi va murabbiy. U 1960 yil 30 oktyabrda tug‘ilgan va 2020 yil 25 noyabrda vafot etgan. Maradona 1986 yilgi Jahon chempionatida Argentina terma jamoasini g‘alabaga olib chiqqan va Xudo qo‘li hamda tarixiy solo goli bilan mashhur bo‘lgan. Klub darajasida Boca Juniors, Barcelona va Napoli klublarida o‘ynagan, ayniqsa, Napoli safida ikki marta Italiya chempioni bo‘lgan. U futbol tarixidagi eng buyuk o‘yinchilardan biri hisoblanadi.",
                                "FUTBOL TIME ⚽️\nJohan Kroyf gollandiyalik afsonaviy futbolchi va murabbiy. U 1947 yil 25 aprelda tug‘ilgan va 2016 yil 24 martda vafot etgan. Kroyf total futbol uslubining asoschilaridan biri bo‘lib, Ayaks va Barselona klublarida o‘ynagan. U uch marta Oltin to‘p sohibi bo‘lgan va Ayaks bilan uch marta Chempionlar Ligasi g‘olibi bo‘lgan. Murabbiy sifatida Barselonani boshqarib, klubga Kroyf falsafasini olib kirgan va tiki taka uslubining rivojlanishiga asos solgan. U futbol tarixidagi eng buyuk o‘yinchilardan biri sifatida tan olingan.",
                                "FUTBOL TIME ⚽️\nKilian Mbappe fransiyalik professional futbolchi, Paris Sen Jermen klubi va Fransiya terma jamoasi hujumchisi. U 1998 yil 20 dekabrda tug‘ilgan. Futbolchilik faoliyatini Monako klubida boshlagan va 2017 yilda PSGga o‘tgan. U bir necha bor Liga 1 chempioni bo‘lgan va Yevropaning eng yaxshi futbolchilaridan biri hisoblanadi. 2018 yilgi Jahon chempionatida Fransiya terma jamoasi bilan g‘olib bo‘lgan va turnirning eng yaxshi yosh futbolchisi deb topilgan. 2022 yilgi Jahon chempionatida eng ko‘p gol urgan futbolchi bo‘lib, finalda xet-trik qayd etgan.",
                                "FUTBOL TIME ⚽️\nErling Haaland norvegiyalik professional futbolchi, Manchester Siti klubi va Norvegiya terma jamoasi hujumchisi. U 2000 yil 21 iyulda tug‘ilgan. Salzburg va Dortmund klublarida porlab, 2022 yilda Manchester Sitiga o‘tgan. Premyer ligada rekord darajada ko‘p gol urgan va Yevropaning eng kuchli hujumchilaridan biri hisoblanadi.",
                                "FUTBOL TIME ⚽️\nFutbol dunyodagi eng mashhur sport turlaridan biri bo‘lib, unda ikkita jamoa to‘pni raqib darvozasiga kiritish orqali g‘alabaga erishishga harakat qiladi. Har bir jamoada 11 nafar o‘yinchi maydonga tushadi. O‘yin 90 daqiqa davom etadi va ikkita bo‘limga bo‘linadi. Futbol qoidalarini FIFA boshqaradi, eng nufuzli turniri esa har to‘rt yilda o‘tkaziladigan Jahon chempionatidir.",
                                "FUTBOL TIME ⚽️\nOltin to‘p futbol dunyosidagi eng nufuzli individual mukofotlardan biri bo‘lib, har yili dunyoning eng yaxshi futbolchisiga topshiriladi. Mukofot 1956 yilda France Football jurnali tomonidan ta’sis etilgan. Dastlab faqat Yevropa futbolchilari uchun mo‘ljallangan bo‘lsa, keyinchalik butun dunyo o‘yinchilari uchun berila boshlandi. Lionel Messi ushbu mukofotni eng ko‘p, 8 marta qo‘lga kiritgan futbolchi hisoblanadi.",
                                "FUTBOL TIME ⚽️\nOltin butsа futbol dunyosidagi eng nufuzli individual mukofotlardan biri bo‘lib, har yili Yevropa chempionatlarida eng ko‘p gol urgan futbolchiga beriladi. Mukofot 1968 yilda ta’sis etilgan va France Football jurnali tomonidan topshiriladi. Gollar liganing kuchliligiga qarab maxsus koeffitsiyent asosida hisoblanadi. Lionel Messi ushbu mukofotni eng ko‘p, 6 marta qo‘lga kiritgan futbolchi hisoblanadi.",
                                "FUTBOL TIME ⚽️\nOltin qo‘lqop mukofoti futbol darvozabonlari uchun beriladigan nufuzli sovrin bo‘lib, turli turnirlarda eng yaxshi darvozabonga topshiriladi. Jahon chempionatida ushbu mukofot 1994 yildan beri FIFA tomonidan taqdim etiladi. Klub darajasida esa UEFA Chempionlar Ligasi va Angliya Premyer Ligasi kabi musobaqalarda ham eng yaxshi darvozabonga Oltin qo‘lqop mukofoti beriladi.",
                                "FUTBOL TIME ⚽️\nJahon chempionati futbol bo‘yicha eng nufuzli turnir bo‘lib, har to‘rt yilda FIFA tomonidan tashkil etiladi. Dastlabki musobaqa 1930 yilda Urugvayda o‘tkazilgan. Turnirda dunyoning eng kuchli terma jamoalari ishtirok etadi. Braziliya eng ko‘p, 5 marta chempion bo‘lgan. So‘nggi Jahon chempionati 2022 yilda Qatarda bo‘lib o‘tgan va Argentina g‘oliblikni qo‘lga kiritgan."
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
