"""
Force-Subscribe (Auth Channel / Auth Group) module.

Agar config.py me AUTH_CHANNEL ya AUTH_GROUP set hai, to user ko
command use karne se pehle un dono ko join karna zaroori hoga.
Khaali ("") rakhne par wo check skip ho jata hai.
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import language

NOT_MEMBER_STATUSES = ("left", "banned", "kicked")


async def _is_member(client, chat_username: str, user_id: int) -> bool:
    """Agar chat_username khaali hai to feature disabled maano (True)."""
    if not chat_username:
        return True
    try:
        member = await client.get_chat_member(chat_username, user_id)
        return member.status.name.lower() not in NOT_MEMBER_STATUSES
    except Exception:
        # User member nahi hai, ya bot khud us channel/group ka member nahi hai
        return False


async def check_subscription(client, message) -> bool:
    """
    True return karta hai agar user dono (jo configured hain) ko join kar chuka hai.
    Nahi to Join buttons ke saath ek message bhejkar False return karta hai.
    """
    if not message.from_user:
        return True

    user_id = message.from_user.id
    chat_id = message.chat.id

    channel_ok = await _is_member(client, config.AUTH_CHANNEL, user_id)
    group_ok = await _is_member(client, config.AUTH_GROUP, user_id)

    if channel_ok and group_ok:
        return True

    buttons = []
    if not channel_ok:
        buttons.append([InlineKeyboardButton(
            language.t(chat_id, "fsub_btn_channel"),
            url=f"https://t.me/{config.AUTH_CHANNEL}",
        )])
    if not group_ok:
        buttons.append([InlineKeyboardButton(
            language.t(chat_id, "fsub_btn_group"),
            url=f"https://t.me/{config.AUTH_GROUP}",
        )])

    await message.reply(
        language.t(chat_id, "fsub_required"),
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )
    return False
