import asyncio
import importlib
import os
 
from aiohttp import web
from pyrogram import Client
from pytgcalls import PyTgCalls
 
import config
import db
import guard
import language
 
# Bot client (BotFather wala bot) - commands handle karega
bot = Client(
    "music_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)
 
# Assistant client (userbot) - voice chat me join karega
assistant = Client(
    "assistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING,
)
 
# PyTgCalls instance - assistant ke through voice chat control karega
call_py = PyTgCalls(assistant)
 
 
async def load_plugins():
    """plugins/ folder ki saari command files load karega"""
    plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"plugins.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                module.register(bot, call_py)
 
 
async def start_dummy_web_server():
    """
    Render 'Web Service' type par ek open HTTP port expect karta hai (health check ke liye),
    lekin ye bot koi webpage serve nahi karta. Ye chhota sa dummy server bas is check ko
    pass karne ke liye hai. Agar Render par 'Background Worker' use kar rahe ho, to
    iski zaroorat nahi hai (PORT env var set nahi hoga to ye khud-ba-khud skip ho jayega).
    """
    port = os.environ.get("PORT")
    if not port:
        return  # Background Worker par PORT set nahi hota - koi zaroorat nahi
 
    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="Bot is running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(port))
    await site.start()
    print(f"Dummy web server port {port} par start ho gaya (Render health-check ke liye).")
 
 
async def main():
    # MongoDB connection test karo aur saara persisted data cache me load karo
    print("MongoDB se connect ho raha hai...")
    await db.ping()
    await guard.load_activated_groups()
    await language.load_chat_languages()
    print(f"MongoDB connected — {len(guard.ACTIVATED_GROUPS)} activated groups aur "
          f"{len(language.CHAT_LANG)} language settings load ho gayi.")
 
    await start_dummy_web_server()
 
    await bot.start()
    await assistant.start()
    await call_py.start()
    await load_plugins()
 
    print(f"{config.BOT_NAME} start ho gaya hai! Bot aur assistant dono online hain.")
    print("Bot ko group me add karo, aur assistant account ko bhi group me add karo.")
 
    await asyncio.Event().wait()  # bot ko hamesha chalte rehne do
 
 
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
 
