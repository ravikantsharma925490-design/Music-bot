import os
import glob
import asyncio
import subprocess

from pyrogram import filters

import config
import language
import guard
import branding

DOWNLOAD_DIR = "spotify_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIFY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIFY_CLIENT_SECRET


def register(bot, call_py):

    @bot.on_message(filters.command("spotify") & filters.group)
    async def spotify_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return

        if len(message.command) < 2:
            await message.reply(language.t(chat_id, "spotify_need_query"))
            return

        query = message.text.split(None, 1)[1].strip()
        status_msg = await message.reply(language.t(chat_id, "spotify_fetching"))

        out_folder = os.path.join(DOWNLOAD_DIR, str(message.id))
        os.makedirs(out_folder, exist_ok=True)

        try:
            await status_msg.edit(language.t(chat_id, "spotify_downloading"))

            process = await asyncio.create_subprocess_exec(
                "spotdl",
                "download",
                query,
                "--output", f"{out_folder}/{{title}}.{{output-ext}}",
                "--format", "mp3",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            mp3_files = glob.glob(os.path.join(out_folder, "*.mp3"))

            if not mp3_files:
                error_text = stderr.decode(errors="ignore")[-500:]
                await status_msg.edit(language.t(chat_id, "spotify_not_found", error=error_text))
                return

            await status_msg.edit(language.t(chat_id, "spotify_sending"))

            for filepath in mp3_files:
                title = os.path.splitext(os.path.basename(filepath))[0]
                await message.reply_audio(
                    filepath,
                    title=title,
                    caption=branding.build_caption(title),
                    reply_markup=branding.build_file_buttons(chat_id),
                )

            await status_msg.delete()

        except FileNotFoundError:
            await status_msg.edit(language.t(chat_id, "spotify_not_installed"))
        except Exception as e:
            await status_msg.edit(language.t(chat_id, "spotify_error", error=e))

        finally:
            for f in glob.glob(os.path.join(out_folder, "*")):
                try:
                    os.remove(f)
                except OSError:
                    pass
            try:
                os.rmdir(out_folder)
            except OSError:
                pass
