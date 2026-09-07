import aiohttp
from pyrogram import filters

import language
import guard


async def search_track(session, query):
    url = f"https://api.lyrics.ovh/suggest/{query}"
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        data = await resp.json()
        results = data.get("data", [])
        if not results:
            return None
        track = results[0]
        return track["artist"]["name"], track["title"]


async def fetch_lyrics(session, artist, title):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        data = await resp.json()
        return data.get("lyrics")


def register(bot, call_py):

    @bot.on_message(filters.command("lyrics") & filters.group)
    async def lyrics_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return

        if len(message.command) < 2:
            await message.reply(language.t(chat_id, "lyrics_need_query"))
            return

        query = message.text.split(None, 1)[1]
        status_msg = await message.reply(language.t(chat_id, "lyrics_searching"))

        try:
            async with aiohttp.ClientSession() as session:
                match = await search_track(session, query)
                if not match:
                    await status_msg.edit(language.t(chat_id, "lyrics_track_not_found"))
                    return

                artist, title = match
                lyrics = await fetch_lyrics(session, artist, title)

                if not lyrics:
                    await status_msg.edit(language.t(chat_id, "lyrics_no_lyrics", title=title, artist=artist))
                    return

            header = f"🎤 **{title}** — {artist}\n\n"
            full_text = header + lyrics.strip()

            if len(full_text) <= 4096:
                await status_msg.edit(full_text)
            else:
                await status_msg.edit(header + language.t(chat_id, "lyrics_long_notice"))
                chunks = [lyrics[i:i + 4000] for i in range(0, len(lyrics), 4000)]
                for chunk in chunks:
                    await message.reply(chunk)

        except Exception as e:
            await status_msg.edit(language.t(chat_id, "lyrics_error", error=e))
