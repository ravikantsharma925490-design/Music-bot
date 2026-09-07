"""
Log Channel module. Agar config.py me LOG_CHANNEL set hai, to important
events (naya group activate hona, errors, etc.) us channel me bhej diye
jaate hain. Khaali rakhne par sab kuch silently skip ho jata hai.
"""

import config


async def send_log(client, text: str):
    if not config.LOG_CHANNEL:
        return
    try:
        await client.send_message(config.LOG_CHANNEL, text)
    except Exception as e:
        print(f"[LOG CHANNEL ERROR] Message bhej nahi paya: {e}")


async def log_new_group(client, message):
    """Jab koi group /start se naya activate hota hai"""
    chat = message.chat
    user = message.from_user

    members_count = "N/A"
    try:
        members_count = await client.get_chat_members_count(chat.id)
    except Exception:
        pass

    text = (
        "🆕 **Naya Group Activate Hua**\n\n"
        f"📛 Group: {chat.title}\n"
        f"🆔 Chat ID: `{chat.id}`\n"
        f"👥 Members: {members_count}\n"
        f"👤 Activate kiya: {user.mention if user else 'Unknown'} "
        f"(`{user.id if user else 'N/A'}`)"
    )
    await send_log(client, text)


async def log_error(client, source: str, error: Exception):
    """Kisi bhi important error ko log channel me bhejne ke liye"""
    text = f"⚠️ **Error in {source}**\n\n`{error}`"
    await send_log(client, text)
