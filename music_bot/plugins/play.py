import random
import yt_dlp
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.stream import StreamAudioEnded

import language
import guard
# queue: [(url, title), ...]
# loop: "off" | "song" | "queue"
# volume: 0-200 (100 = normal)
QUEUES = {}


def get_state(chat_id):
    if chat_id not in QUEUES:
        QUEUES[chat_id] = {
            "queue": [],
            "playing": False,
            "current": None,
            "current_url": None,
            "loop": "off",
            "volume": 100,
        }
    return QUEUES[chat_id]


def get_audio_info(query: str, playlist: bool = False):
    """YouTube se audio stream URL(s) aur title(s) nikaalta hai.
    playlist=True hone par poori playlist ki entries return karta hai."""
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": not playlist,
        "quiet": True,
        "default_search": "ytsearch",
        "nocheckcertificate": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            entries = [e for e in info["entries"] if e]
            if playlist:
                return [(e["url"], e["title"]) for e in entries]
            info = entries[0]
        return info["url"], info["title"], info.get("duration", 0)


def player_buttons(chat_id, paused=False, loop_mode="off"):
    """Player message ke neeche control buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("▶️ Resume" if paused else "⏸ Pause", callback_data=f"mp_pause_{chat_id}"),
            InlineKeyboardButton("⏭ Skip", callback_data=f"mp_skip_{chat_id}"),
            InlineKeyboardButton("⏹ Stop", callback_data=f"mp_stop_{chat_id}"),
        ],
        [
            InlineKeyboardButton("🔀 Shuffle", callback_data=f"mp_shuffle_{chat_id}"),
            InlineKeyboardButton(loop_label(chat_id, loop_mode), callback_data=f"mp_loop_{chat_id}"),
        ],
    ])


def loop_label(chat_id, mode):
    return language.t(chat_id, f"loop_{mode}")


def register(bot, call_py):

    async def start_next(chat_id, status_msg=None):
        """Queue se agla gaana start karta hai (loop mode dhyan me rakh kar)"""
        state = get_state(chat_id)

        if state["loop"] == "song" and state["current_url"]:
            audio_url, title = state["current_url"], state["current"]
        elif state["queue"]:
            audio_url, title = state["queue"].pop(0)
        else:
            state["playing"] = False
            await call_py.leave_group_call(chat_id)
            return

        await call_py.change_stream(chat_id, AudioPiped(audio_url))
        state["current"], state["current_url"] = title, audio_url
        state["playing"] = True

        if state["loop"] == "queue" and state.get("_last_played"):
            state["queue"].append(state["_last_played"])
        state["_last_played"] = (audio_url, title)

        if status_msg:
            await status_msg.edit(
                language.t(chat_id, "play_now_playing", title=title),
                reply_markup=player_buttons(chat_id, loop_mode=state["loop"]),
            )

    @bot.on_message(filters.command("play") & filters.group)
    async def play_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return

        if len(message.command) < 2:
            await message.reply(language.t(chat_id, "play_need_query"))
            return

        query = message.text.split(None, 1)[1]
        state = get_state(chat_id)
        is_playlist = "list=" in query or "playlist" in query.lower()

        status_msg = await message.reply(language.t(chat_id, "play_searching"))

        try:
            if is_playlist:
                entries = get_audio_info(query, playlist=True)
                if not entries:
                    await status_msg.edit(language.t(chat_id, "play_playlist_empty"))
                    return
                first_url, first_title = entries[0]
                remaining = entries[1:]
            else:
                first_url, first_title, _ = get_audio_info(query)
                remaining = []
        except Exception as e:
            await status_msg.edit(language.t(chat_id, "play_not_found", error=e))
            return

        try:
            if state["playing"]:
                state["queue"].append((first_url, first_title))
                state["queue"].extend(remaining)
                extra = language.t(chat_id, "play_added_playlist_extra", count=len(remaining)) if remaining else ""
                await status_msg.edit(
                    language.t(chat_id, "play_added_queue", title=first_title) + extra
                )
            else:
                await call_py.join_group_call(chat_id, AudioPiped(first_url))
                state["current"], state["current_url"] = first_title, first_url
                state["playing"] = True
                state["queue"].extend(remaining)
                extra = language.t(chat_id, "play_playlist_extra", count=len(remaining)) if remaining else ""
                await status_msg.edit(
                    language.t(chat_id, "play_now_playing", title=first_title) + extra,
                    reply_markup=player_buttons(chat_id, loop_mode=state["loop"]),
                )
        except Exception as e:
            await status_msg.edit(language.t(chat_id, "play_join_error", error=e))

    @bot.on_message(filters.command(["pause"]) & filters.group)
    async def pause_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        try:
            await call_py.pause_stream(chat_id)
            await message.reply(language.t(chat_id, "pause_done"))
        except Exception as e:
            await message.reply(language.t(chat_id, "generic_error", error=e))

    @bot.on_message(filters.command(["resume"]) & filters.group)
    async def resume_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        try:
            await call_py.resume_stream(chat_id)
            await message.reply(language.t(chat_id, "resume_done"))
        except Exception as e:
            await message.reply(language.t(chat_id, "generic_error", error=e))

    @bot.on_message(filters.command(["stop", "end"]) & filters.group)
    async def stop_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        try:
            await call_py.leave_group_call(chat_id)
            QUEUES.pop(chat_id, None)
            await message.reply(language.t(chat_id, "stop_done"))
        except Exception as e:
            await message.reply(language.t(chat_id, "generic_error", error=e))

    @bot.on_message(filters.command(["skip", "next"]) & filters.group)
    async def skip_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        state = get_state(chat_id)
        if not state["queue"] and state["loop"] != "song":
            await message.reply(language.t(chat_id, "skip_empty"))
            return
        await start_next(chat_id, status_msg=await message.reply(language.t(chat_id, "skip_doing")))

    @bot.on_message(filters.command(["queue", "q"]) & filters.group)
    async def queue_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        state = QUEUES.get(chat_id)
        if not state or not state["playing"]:
            await message.reply(language.t(chat_id, "queue_empty"))
            return
        text = language.t(chat_id, "queue_header", title=state["current"])
        text += f"{loop_label(chat_id, state['loop'])}\n\n"
        if state["queue"]:
            text += language.t(chat_id, "queue_upcoming")
            for i, (_, title) in enumerate(state["queue"], start=1):
                text += f"{i}. {title}\n"
        else:
            text += language.t(chat_id, "queue_none")
        await message.reply(text)

    @bot.on_message(filters.command("shuffle") & filters.group)
    async def shuffle_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        state = get_state(chat_id)
        if len(state["queue"]) < 2:
            await message.reply(language.t(chat_id, "shuffle_need_more"))
            return
        random.shuffle(state["queue"])
        await message.reply(language.t(chat_id, "shuffle_done"))

    @bot.on_message(filters.command("loop") & filters.group)
    async def loop_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        state = get_state(chat_id)
        modes = ["off", "song", "queue"]

        if len(message.command) > 1 and message.command[1].lower() in modes:
            state["loop"] = message.command[1].lower()
        else:
            state["loop"] = modes[(modes.index(state["loop"]) + 1) % len(modes)]

        await message.reply(language.t(chat_id, "loop_set", label=loop_label(chat_id, state["loop"])))

    @bot.on_message(filters.command("volume") & filters.group)
    async def volume_cmd(client, message):
        chat_id = message.chat.id
        if not await guard.check_ready(client, message):
            return
        state = get_state(chat_id)

        if len(message.command) < 2 or not message.command[1].isdigit():
            await message.reply(language.t(chat_id, "volume_current", vol=state["volume"]))
            return

        vol = int(message.command[1])
        if not (0 <= vol <= 200):
            await message.reply(language.t(chat_id, "volume_range_error"))
            return

        try:
            await call_py.change_volume_call(chat_id, vol)
            state["volume"] = vol
            await message.reply(language.t(chat_id, "volume_set", vol=vol))
        except Exception as e:
            await message.reply(language.t(chat_id, "generic_error", error=e))

    # ---------- Inline button handlers ----------

    @bot.on_callback_query(filters.regex(r"^mp_"))
    async def player_buttons_handler(client, callback: CallbackQuery):
        action, chat_id = callback.data.split("_", 2)[1], int(callback.data.split("_")[-1])
        state = get_state(chat_id)

        try:
            if action == "pause":
                if state.get("_paused"):
                    await call_py.resume_stream(chat_id)
                    state["_paused"] = False
                    await callback.answer(language.t(chat_id, "resume_done"))
                else:
                    await call_py.pause_stream(chat_id)
                    state["_paused"] = True
                    await callback.answer(language.t(chat_id, "pause_done"))
                await callback.message.edit_reply_markup(
                    player_buttons(chat_id, paused=state["_paused"], loop_mode=state["loop"])
                )

            elif action == "skip":
                if not state["queue"] and state["loop"] != "song":
                    await callback.answer(language.t(chat_id, "skip_empty"), show_alert=True)
                    return
                await start_next(chat_id, status_msg=callback.message)
                await callback.answer(language.t(chat_id, "skip_doing"))

            elif action == "stop":
                await call_py.leave_group_call(chat_id)
                QUEUES.pop(chat_id, None)
                await callback.message.edit(language.t(chat_id, "stop_done"))
                await callback.answer(language.t(chat_id, "stop_done"))

            elif action == "shuffle":
                if len(state["queue"]) < 2:
                    await callback.answer(language.t(chat_id, "shuffle_need_more"), show_alert=True)
                    return
                random.shuffle(state["queue"])
                await callback.answer(language.t(chat_id, "shuffle_done"))

            elif action == "loop":
                modes = ["off", "song", "queue"]
                state["loop"] = modes[(modes.index(state["loop"]) + 1) % len(modes)]
                await callback.answer(loop_label(chat_id, state["loop"]))
                kb = player_buttons(chat_id, paused=state.get("_paused", False), loop_mode=state["loop"])
                await callback.message.edit_reply_markup(kb)

        except Exception as e:
            await callback.answer(language.t(chat_id, "generic_error", error=e), show_alert=True)

    # Jab gaana khatam ho jaye to agla apne aap bajao
    @call_py.on_stream_end()
    async def on_stream_end(client, update):
        if isinstance(update, StreamAudioEnded):
            await start_next(update.chat_id)
