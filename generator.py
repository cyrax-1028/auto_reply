from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# API ma'lumotlari
API_ID = input("API ID kiriting: ")
API_HASH = input("API Hash kiriting: ")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    session_string = client.session.save()
    print("\n💾 String Session:")
    print(session_string)
    print("\n⚠️ Ushbu ma'lumotni hech kimga bermang!")
