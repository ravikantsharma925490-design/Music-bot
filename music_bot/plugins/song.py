import os
import yt_dlp
from pyrogram import filters

import language
import guard
import branding

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def register(bot, call_py):

    @bot.on_message(filters.command("song") & filters.group)
    async def song_cmd(client, message):
        """Gaana MP3 file ke roop me group me bhejta hai (voice chat use nahi karta)"""
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return

        if len(message.command) < 2:
            await message.reply(language.t(chat_id, "song_need_query"))
            return

        query = message.text.split(None, 1)[1]
        status_msg = await message.reply(language.t(chat_id, "song_downloading"))

        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "default_search": "ytsearch",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                if "entries" in info:
                    info = info["entries"][0]
                title = info["title"]
                filepath = ydl.prepare_filename(info)
                filepath = os.path.splitext(filepath)[0] + ".mp3"

            await status_msg.edit(language.t(chat_id, "song_sending"))
            await message.reply_audio(
                filepath,
                title=title,
                caption=branding.build_caption(title),
                reply_markup=branding.build_file_buttons(chat_id),
            )
            await status_msg.delete()

            os.remove(filepath)

        except Exception as e:
            await status_msg.edit(language.t(chat_id, "song_error", error=e))
