import os
import yt_dlp
from pyrogram import filters

import language
import guard
import branding

DOWNLOAD_DIR = "video_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Telegram bot API se 2GB tak file bhej sakte hain (local bot API server ke saath),
# default cloud bot API par limit 50MB hoti hai. Isliye 720p tak hi download karte hain
# taaki file size manageable rahe.
MAX_HEIGHT = 720


def register(bot, call_py):

    @bot.on_message(filters.command(["video", "vid"]) & filters.group)
    async def video_cmd(client, message):
        """Video ko MP4 file ke roop me group me download karke bhejta hai"""
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return

        if len(message.command) < 2:
            await message.reply(language.t(chat_id, "video_need_query"))
            return

        query = message.text.split(None, 1)[1]
        status_msg = await message.reply(language.t(chat_id, "video_downloading"))

        ydl_opts = {
            "format": f"bestvideo[height<={MAX_HEIGHT}][ext=mp4]+bestaudio[ext=m4a]/best[height<={MAX_HEIGHT}][ext=mp4]/best",
            "noplaylist": True,
            "quiet": True,
            "default_search": "ytsearch",
            "merge_output_format": "mp4",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        }

        filepath = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                if "entries" in info:
                    info = info["entries"][0]
                title = info["title"]
                duration = info.get("duration", 0)
                filepath = ydl.prepare_filename(info)
                if not filepath.endswith(".mp4"):
                    filepath = os.path.splitext(filepath)[0] + ".mp4"

            file_size = os.path.getsize(filepath)
            if file_size > 2 * 1024 * 1024 * 1024:  # 2GB
                await status_msg.edit(language.t(chat_id, "video_too_large"))
                os.remove(filepath)
                return

            await status_msg.edit(language.t(chat_id, "video_sending"))
            await message.reply_video(
                filepath,
                caption=branding.build_caption(title),
                duration=duration,
                supports_streaming=True,
                reply_markup=branding.build_file_buttons(chat_id),
            )
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(language.t(chat_id, "video_error", error=e))
        finally:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)

    @bot.on_message(filters.command(["vlink", "videolink"]) & filters.group)
    async def vlink_cmd(client, message):
        """Video ko download kiye bina, seedha temporary streaming/download link deta hai"""
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return

        if len(message.command) < 2:
            await message.reply(language.t(chat_id, "vlink_need_query"))
            return

        query = message.text.split(None, 1)[1]
        status_msg = await message.reply(language.t(chat_id, "vlink_fetching"))

        ydl_opts = {
            "format": f"best[height<={MAX_HEIGHT}][ext=mp4]/best",
            "noplaylist": True,
            "quiet": True,
            "default_search": "ytsearch",
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if "entries" in info:
                    info = info["entries"][0]
                title = info["title"]
                direct_url = info["url"]

            await status_msg.edit(
                language.t(chat_id, "vlink_result", title=title, url=direct_url),
                disable_web_page_preview=False,
            )

        except Exception as e:
            await status_msg.edit(language.t(chat_id, "vlink_error", error=e))
