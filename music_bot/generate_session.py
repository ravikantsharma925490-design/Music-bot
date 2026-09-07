"""
Ye script sirf EK BAAR chalani hai — assistant account ki SESSION_STRING
generate karne ke liye. Ye string config.py me daalni hai.

Chalane ka tarika:
    python generate_session.py

Phone number wahi daalna jo assistant/userbot account ke liye use karna hai
(BOT account ka phone number NAHI daalna - ye normal Telegram account hona chahiye).
"""

from pyrogram import Client

API_ID = int(input("Apna API_ID daalo: "))
API_HASH = input("Apna API_HASH daalo: ")

with Client(name="session_gen", api_id=API_ID, api_hash=API_HASH) as app:
    session_string = app.export_session_string()
    print("\n\n================ YE HAI TUMHARI SESSION STRING ================\n")
    print(session_string)
    print("\n=================================================================")
    print("Ise config.py ke SESSION_STRING variable me paste kar do.\n")
