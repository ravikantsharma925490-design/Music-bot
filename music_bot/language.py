"""
Central translation module. Har group apni language choose kar sakta hai
(/language command se). Default: Hindi (Hinglish).
"""

import db

# Har chat ki language yahan store hoti hai (runtime memory me cache,
# MongoDB se load hoti hai aur wahin persist hoti hai)
CHAT_LANG = {}

DEFAULT_LANG = "hi"

STRINGS = {
    "hi": {
        "play_need_query": "❗ Gaane ka naam ya YouTube link do.\nExample: `/play tum hi ho`",
        "play_searching": "🔎 Gaana dhoonda ja raha hai...",
        "play_not_found": "❌ Gaana nahi mil paya: {error}",
        "play_playlist_empty": "❌ Playlist khaali hai ya nahi mili.",
        "play_added_queue": "➕ Queue me add ho gaya: **{title}**",
        "play_added_playlist_extra": "\n➕ Aur {count} gaane bhi playlist se add ho gaye.",
        "play_now_playing": "🎵 **Ab baj raha hai:** {title}",
        "play_playlist_extra": "\n➕ {count} aur gaane queue me hain (playlist se).",
        "play_join_error": "❌ Voice chat me join nahi ho paya: {error}\n\nCheck karo ki group me voice chat active hai aur assistant account group me hai.",
        "pause_done": "⏸ Music pause kar diya gaya.",
        "resume_done": "▶️ Music resume kar diya gaya.",
        "stop_done": "⏹ Music band kar diya gaya, bot voice chat se nikal gaya.",
        "skip_empty": "📭 Queue khaali hai, koi agla gaana nahi hai.",
        "skip_doing": "⏭ Skip ho raha hai...",
        "queue_empty": "📭 Kuch bhi nahi chal raha.",
        "queue_header": "🎶 **Ab baj raha hai:** {title}\n",
        "queue_upcoming": "**Aage ki queue:**\n",
        "queue_none": "Queue me aur kuch nahi hai.",
        "shuffle_need_more": "📭 Shuffle karne ke liye queue me kam se kam 2 gaane chahiye.",
        "shuffle_done": "🔀 Queue shuffle kar di gayi!",
        "loop_set": "{label} set ho gaya.",
        "loop_off": "🔁 Loop: Off",
        "loop_song": "🔂 Loop: Song",
        "loop_queue": "🔁 Loop: Queue",
        "volume_current": "🔊 Current volume: **{vol}%**\nExample: `/volume 150`",
        "volume_range_error": "❗ Volume 0 se 200 ke beech hona chahiye.",
        "volume_set": "🔊 Volume set kar diya: **{vol}%**",
        "generic_error": "❌ Error: {error}",
        "song_need_query": "❗ Gaane ka naam do.\nExample: `/song kesariya`",
        "song_downloading": "🔎 Gaana download ho raha hai, thoda ruko...",
        "song_sending": "📤 Bhej raha hoon...",
        "song_error": "❌ Kuch galat ho gaya: {error}",
        "spotify_need_query": "❗ Spotify link ya gaane ka naam do.\nExample: `/spotify https://open.spotify.com/track/...`\nYa: `/spotify Tum Hi Ho`",
        "spotify_fetching": "🔎 Spotify se details nikaali ja rahi hain...",
        "spotify_downloading": "⬇️ Download ho raha hai, thoda ruko...",
        "spotify_sending": "📤 Bhej raha hoon...",
        "spotify_not_found": "❌ Gaana nahi mil paya ya download fail ho gaya.\n\nDetail: `{error}`",
        "spotify_not_installed": "❌ `spotdl` install nahi hai. Terminal me ye chalao:\n`pip install spotdl`",
        "spotify_error": "❌ Kuch galat ho gaya: {error}",
        "lyrics_need_query": "❗ Gaane ka naam do.\nExample: `/lyrics Tum Hi Ho`",
        "lyrics_searching": "🔎 Lyrics dhoondi ja rahi hain...",
        "lyrics_track_not_found": "❌ Ye gaana nahi mila.",
        "lyrics_no_lyrics": "❌ **{title}** ({artist}) ki lyrics nahi mili.",
        "lyrics_error": "❌ Kuch galat ho gaya: {error}",
        "lyrics_long_notice": "(lyrics lambi hai, neeche jaari hai...)",
        "lang_current": "🌐 Abhi is group ki language hai: **Hindi**\nBadalne ke liye: `/language english`",
        "lang_set": "✅ Language set kar di gayi: **{lang_name}**",
        "lang_invalid": "❗ Sirf `hindi` ya `english` choose kar sakte ho.\nExample: `/language english`",
        "video_need_query": "❗ Video ka naam ya YouTube link do.\nExample: `/video believer imagine dragons`",
        "video_downloading": "🔎 Video download ho raha hai, thoda ruko (bade video me time lag sakta hai)...",
        "video_sending": "📤 Video bhej raha hoon...",
        "video_too_large": "❌ Ye video Telegram ki file size limit (2GB) se bada hai, isliye bheja nahi ja sakta.\nInstead `/vlink` try karo, wo seedha streaming link degа.",
        "video_error": "❌ Kuch galat ho gaya: {error}",
        "vlink_need_query": "❗ Video ka naam ya YouTube link do.\nExample: `/vlink believer imagine dragons`",
        "vlink_fetching": "🔎 Streaming link nikaala ja raha hai...",
        "vlink_result": "🎬 **{title}**\n\n🔗 [Yahan click karke seedha stream/download karo]({url})\n\n⚠️ Ye link kuch ghanto me expire ho sakta hai (YouTube ki taraf se).",
        "vlink_error": "❌ Link nahi mil paya: {error}",
        "start_private": "👋 Namaste {name}!\n\nMain ek Music Bot hoon 🎶\nMujhe kisi bhi group me add karo aur wahan `/play`, `/song`, `/spotify`, `/video` jaise commands se music/video enjoy karo.",
        "start_group": "👋 **Bot active ho gaya hai is group me!**\n\n🎵 `/play` — voice chat me gaana stream karo\n📥 `/song` — MP3 file paao\n🟢 `/spotify` — Spotify se gaana paao\n🎬 `/video` — video download karo\n📜 `/help` — sabhi commands dekho\n\nChalo shuru karte hain!",
        "btn_help": "📜 Sabhi Commands",
        "btn_add_group": "➕ Group me add karo",
        "btn_language": "🌐 Language",
        "help_title": "📜 **Sabhi Commands:**\n\n",
        "help_rules_title": "\n\n📋 **Bot Use Karne Ke Rules:**\n",
        "help_rules": (
            "1️⃣ Bot ko group me **Admin** banana zaroori hai\n"
            "2️⃣ Group me ek baar `/start` bhejo (sirf ek baar, phir hamesha ke liye activate rahega)\n"
            "3️⃣ Voice chat streaming (`/play`) ke liye group me voice chat pehle se ON honi chahiye\n"
            "4️⃣ Agar Auth Channel/Group set hai, to pehle unhe join karo, tabhi commands chalengi\n"
            "5️⃣ Sabhi commands sirf **group chat** me kaam karte hain"
        ),
        "not_started": "⚠️ Is group me bot abhi tak `/start` se activate nahi hua hai.\nPehle group me `/start` bhejo (sirf ek baar karna hai).",
        "bot_not_admin": "⚠️ Mujhe pehle is group ka **Admin** banao, tabhi main kaam kar paunga.\nAdmin banane ke baad koi bhi command dubara try karo.",
        "start_needs_admin": "⚠️ Activate karne ke liye pehle mujhe group ka **Admin** banao (Voice chats manage karne ki permission ke saath), phir `/start` dubara bhejo.",
        "start_already_active": "✅ Ye group pehle se activate hai! Sab commands kaam kar rahe hain.",
        "fsub_required": "⚠️ Bot use karne ke liye pehle neeche diye gaye channel/group ko join karo, phir dubara command try karo.",
        "fsub_btn_channel": "📢 Channel Join Karo",
        "fsub_btn_group": "👥 Group Join Karo",
        "btn_join_channel": "📢 Join Channel",
        "btn_join_group": "👥 Join Group",
        "btn_about": "ℹ️ About",
        "about_text": (
            "ℹ️ **Bot Ke Baare Me**\n\n"
            f"🎶 Naam: {{bot_name}}\n"
            "🛠 Banaya gaya: Pyrogram + PyTgCalls se\n"
            "🗄️ Database: MongoDB\n"
            "🌐 Language: Hindi / English\n\n"
            "Voice chat streaming, YouTube/Spotify download, video download, "
            "lyrics — sab kuch ek hi bot me!"
        ),
    },
    "en": {
        "play_need_query": "❗ Give a song name or YouTube link.\nExample: `/play tum hi ho`",
        "play_searching": "🔎 Searching for the song...",
        "play_not_found": "❌ Couldn't find that song: {error}",
        "play_playlist_empty": "❌ Playlist is empty or couldn't be found.",
        "play_added_queue": "➕ Added to queue: **{title}**",
        "play_added_playlist_extra": "\n➕ {count} more songs from the playlist were also added.",
        "play_now_playing": "🎵 **Now playing:** {title}",
        "play_playlist_extra": "\n➕ {count} more songs from the playlist are in the queue.",
        "play_join_error": "❌ Couldn't join the voice chat: {error}\n\nMake sure the voice chat is active in the group and the assistant account is a member.",
        "pause_done": "⏸ Music paused.",
        "resume_done": "▶️ Music resumed.",
        "stop_done": "⏹ Music stopped, bot left the voice chat.",
        "skip_empty": "📭 Queue is empty, no next song.",
        "skip_doing": "⏭ Skipping...",
        "queue_empty": "📭 Nothing is playing right now.",
        "queue_header": "🎶 **Now playing:** {title}\n",
        "queue_upcoming": "**Up next:**\n",
        "queue_none": "Nothing else in the queue.",
        "shuffle_need_more": "📭 Need at least 2 songs in queue to shuffle.",
        "shuffle_done": "🔀 Queue shuffled!",
        "loop_set": "{label} set.",
        "loop_off": "🔁 Loop: Off",
        "loop_song": "🔂 Loop: Song",
        "loop_queue": "🔁 Loop: Queue",
        "volume_current": "🔊 Current volume: **{vol}%**\nExample: `/volume 150`",
        "volume_range_error": "❗ Volume must be between 0 and 200.",
        "volume_set": "🔊 Volume set to: **{vol}%**",
        "generic_error": "❌ Error: {error}",
        "song_need_query": "❗ Give a song name.\nExample: `/song kesariya`",
        "song_downloading": "🔎 Downloading the song, please wait...",
        "song_sending": "📤 Sending...",
        "song_error": "❌ Something went wrong: {error}",
        "spotify_need_query": "❗ Give a Spotify link or song name.\nExample: `/spotify https://open.spotify.com/track/...`\nOr: `/spotify Tum Hi Ho`",
        "spotify_fetching": "🔎 Fetching details from Spotify...",
        "spotify_downloading": "⬇️ Downloading, please wait...",
        "spotify_sending": "📤 Sending...",
        "spotify_not_found": "❌ Song not found or download failed.\n\nDetail: `{error}`",
        "spotify_not_installed": "❌ `spotdl` isn't installed. Run this in terminal:\n`pip install spotdl`",
        "spotify_error": "❌ Something went wrong: {error}",
        "lyrics_need_query": "❗ Give a song name.\nExample: `/lyrics Tum Hi Ho`",
        "lyrics_searching": "🔎 Searching for lyrics...",
        "lyrics_track_not_found": "❌ Couldn't find that song.",
        "lyrics_no_lyrics": "❌ Couldn't find lyrics for **{title}** ({artist}).",
        "lyrics_error": "❌ Something went wrong: {error}",
        "lyrics_long_notice": "(lyrics are long, continued below...)",
        "lang_current": "🌐 This group's language is currently: **English**\nTo change: `/language hindi`",
        "lang_set": "✅ Language set to: **{lang_name}**",
        "lang_invalid": "❗ You can only choose `hindi` or `english`.\nExample: `/language english`",
        "video_need_query": "❗ Give a video name or YouTube link.\nExample: `/video believer imagine dragons`",
        "video_downloading": "🔎 Downloading the video, please wait (larger videos take longer)...",
        "video_sending": "📤 Sending the video...",
        "video_too_large": "❌ This video is larger than Telegram's file size limit (2GB), so it can't be sent.\nTry `/vlink` instead — it gives a direct streaming link.",
        "video_error": "❌ Something went wrong: {error}",
        "vlink_need_query": "❗ Give a video name or YouTube link.\nExample: `/vlink believer imagine dragons`",
        "vlink_fetching": "🔎 Fetching the streaming link...",
        "vlink_result": "🎬 **{title}**\n\n🔗 [Click here to stream/download directly]({url})\n\n⚠️ This link may expire in a few hours (YouTube-side expiry).",
        "vlink_error": "❌ Couldn't get the link: {error}",
        "start_private": "👋 Hello {name}!\n\nI'm a Music Bot 🎶\nAdd me to any group and enjoy music/video there using commands like `/play`, `/song`, `/spotify`, `/video`.",
        "start_group": "👋 **Bot is now active in this group!**\n\n🎵 `/play` — stream music in voice chat\n📥 `/song` — get an MP3 file\n🟢 `/spotify` — get a song from Spotify\n🎬 `/video` — download a video\n📜 `/help` — see all commands\n\nLet's get started!",
        "btn_help": "📜 All Commands",
        "btn_add_group": "➕ Add to Group",
        "btn_language": "🌐 Language",
        "help_title": "📜 **All Commands:**\n\n",
        "help_rules_title": "\n\n📋 **Rules for Using the Bot:**\n",
        "help_rules": (
            "1️⃣ The bot must be made **Admin** in the group\n"
            "2️⃣ Send `/start` once in the group (only once — it stays activated forever after)\n"
            "3️⃣ For voice chat streaming (`/play`), a voice chat must already be ON in the group\n"
            "4️⃣ If an Auth Channel/Group is set, join it first — commands won't work otherwise\n"
            "5️⃣ All commands only work in **group chats**"
        ),
        "not_started": "⚠️ The bot hasn't been activated in this group yet.\nSend `/start` in the group first (only needed once).",
        "bot_not_admin": "⚠️ Please make me an **Admin** in this group first, then I'll be able to work.\nTry the command again after making me admin.",
        "start_needs_admin": "⚠️ To activate, please make me an **Admin** in this group first (with permission to manage voice chats), then send `/start` again.",
        "start_already_active": "✅ This group is already activated! All commands are working.",
        "fsub_required": "⚠️ Please join the channel/group below to use this bot, then try the command again.",
        "fsub_btn_channel": "📢 Join Channel",
        "fsub_btn_group": "👥 Join Group",
        "btn_join_channel": "📢 Join Channel",
        "btn_join_group": "👥 Join Group",
        "btn_about": "ℹ️ About",
        "about_text": (
            "ℹ️ **About This Bot**\n\n"
            f"🎶 Name: {{bot_name}}\n"
            "🛠 Built with: Pyrogram + PyTgCalls\n"
            "🗄️ Database: MongoDB\n"
            "🌐 Language: Hindi / English\n\n"
            "Voice chat streaming, YouTube/Spotify downloads, video downloads, "
            "lyrics — all in one bot!"
        ),
    },
}


def get_lang(chat_id):
    return CHAT_LANG.get(chat_id, DEFAULT_LANG)


async def set_lang(chat_id, lang_code):
    """Cache turant update hoti hai, aur MongoDB me bhi permanently save ho jata hai"""
    CHAT_LANG[chat_id] = lang_code
    await db.set_chat_language(chat_id, lang_code)


async def load_chat_languages():
    """Bot start hote hi MongoDB se saari groups ki language settings cache me load karo"""
    global CHAT_LANG
    CHAT_LANG = await db.get_all_chat_languages()


def t(chat_id, key, **kwargs):
    """Given chat's current language me translated, formatted string return karta hai"""
    lang = get_lang(chat_id)
    template = STRINGS.get(lang, STRINGS[DEFAULT_LANG]).get(key, key)
    return template.format(**kwargs) if kwargs else template
