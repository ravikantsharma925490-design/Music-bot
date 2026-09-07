"""
Guard module:
1. Group ek baar /start se activate hone ke baad hamesha ke liye activate rehta hai
   (MongoDB me persist hota hai — bot restart ya kahin bhi deploy karne par bhi yaad rehta hai).
2. Koi bhi music/video command tabhi kaam karega jab:
   a. User ne Auth Channel/Group join kiya ho (agar set hai)
   b. Group /start se activate ho chuka ho
   c. Bot khud us group me ADMIN ho
"""

import language
import fsub
import db

# In-memory cache — fast access ke liye. Startup par MongoDB se load hoti hai
# (load_activated_groups() call karke), aur har naye activation par turant update hoti hai.
ACTIVATED_GROUPS = set()


async def load_activated_groups():
    """Bot start hote hi MongoDB se saari activated groups cache me load karo"""
    global ACTIVATED_GROUPS
    ACTIVATED_GROUPS = await db.get_all_activated_groups()


def is_activated(chat_id) -> bool:
    return chat_id in ACTIVATED_GROUPS


async def activate(chat_id):
    """Group ko hamesha ke liye activate karta hai (MongoDB + cache dono me save hota hai)"""
    ACTIVATED_GROUPS.add(chat_id)
    await db.add_activated_group(chat_id)


async def is_bot_admin(client, chat_id) -> bool:
    try:
        member = await client.get_chat_member(chat_id, "me")
        return member.status.name.lower() in ("administrator", "owner", "creator")
    except Exception:
        return False


async def check_ready(client, message) -> bool:
    """
    Har group command ke shuru me call karo. Agar user ne Auth Channel/Group
    join nahi kiya, group activate nahi hai, ya bot admin nahi hai — to
    user ko batakar False return karta hai. Command wahin rukk jani chahiye.
    """
    chat_id = message.chat.id

    if not await fsub.check_subscription(client, message):
        return False

    if not is_activated(chat_id):
        await message.reply(language.t(chat_id, "not_started"))
        return False

    if not await is_bot_admin(client, chat_id):
        await message.reply(language.t(chat_id, "bot_not_admin"))
        return False

    return True
