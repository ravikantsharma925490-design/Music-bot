"""
Branding helper — file sends (/song, /video, /spotify) ke saath stylish
caption ("Powered By" + bot naam) aur Join Channel button attach karta hai.

Sirf branding ke liye hai — koi evasion trick (auto-delete warnings,
"forward kar lo" jaisi cheezein) yahan nahi hai.
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config


def build_caption(title: str) -> str:
    """Gaana/video ke title ke saath ek stylish caption banata hai"""
    return (
        f"🎬 **{title}**\n\n"
        f"⚡ Powered By: **{config.BOT_NAME}**"
    )


def build_file_buttons(chat_id):
    """Agar UPDATES_CHANNEL set hai to Join Channel button return karta hai, warna None"""
    if not config.UPDATES_CHANNEL:
        return None
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Join Updates Channel 📌", url=f"https://t.me/{config.UPDATES_CHANNEL}")]
    ])
