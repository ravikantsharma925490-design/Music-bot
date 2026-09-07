from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import language
import guard
import fsub
import logger
import config

HELP_TEXT_KEY_COMMANDS = [
    "/play <naam/link> — Voice chat me live gaana (playlist bhi)",
    "/pause, /resume, /skip, /stop — Voice chat control",
    "/queue — Current queue dekho",
    "/shuffle, /loop — Queue shuffle/loop karo",
    "/volume <0-200> — Volume set karo",
    "/lyrics <naam> — Gaane ki lyrics",
    "/song <naam> — YouTube se MP3 file",
    "/spotify <link/naam> — Spotify se MP3 file",
    "/video <naam/link> — Video MP4 file",
    "/vlink <naam/link> — Direct streaming link",
    "/language hindi|english — Language switch karo",
]


def build_help_text(chat_id):
    text = language.t(chat_id, "help_title")
    text += "\n".join(f"• `{c.split(' — ')[0]}` — {c.split(' — ', 1)[1]}" for c in HELP_TEXT_KEY_COMMANDS)
    text += language.t(chat_id, "help_rules_title")
    text += language.t(chat_id, "help_rules")
    return text


def build_start_menu_buttons(chat_id, bot_username, in_group: bool):
    """
    Grid-style button layout (jaise popular bots me hota hai):
    Row 1: Join Channel | Join Group   (agar config me set hain)
    Row 2: Help | About
    Row 3: Add to Group (sirf private chat me) | Language
    """
    rows = []

    join_row = []
    if config.UPDATES_CHANNEL:
        join_row.append(InlineKeyboardButton(
            language.t(chat_id, "btn_join_channel"),
            url=f"https://t.me/{config.UPDATES_CHANNEL}",
        ))
    if config.SUPPORT_GROUP:
        join_row.append(InlineKeyboardButton(
            language.t(chat_id, "btn_join_group"),
            url=f"https://t.me/{config.SUPPORT_GROUP}",
        ))
    if join_row:
        rows.append(join_row)

    rows.append([
        InlineKeyboardButton(language.t(chat_id, "btn_help"), callback_data="show_help"),
        InlineKeyboardButton(language.t(chat_id, "btn_about"), callback_data="show_about"),
    ])

    last_row = []
    if not in_group:
        last_row.append(InlineKeyboardButton(
            language.t(chat_id, "btn_add_group"),
            url=f"https://t.me/{bot_username}?startgroup=true",
        ))
    last_row.append(InlineKeyboardButton(language.t(chat_id, "btn_language"), callback_data="show_lang_options"))
    rows.append(last_row)

    return InlineKeyboardMarkup(rows)


def register(bot, call_py):

    @bot.on_message(filters.command("start"))
    async def start_cmd(client, message):
        chat_id = message.chat.id

        if not await fsub.check_subscription(client, message):
            return

        if message.chat.type == "private":
            name = message.from_user.first_name if message.from_user else "there"
            buttons = build_start_menu_buttons(chat_id, client.me.username, in_group=False)
            await message.reply(
                language.t(chat_id, "start_private", name=name),
                reply_markup=buttons,
            )
        else:
            # Group me /start karne par: bot ADMIN hai ya nahi check karo,
            # aur ek baar activate hone ke baad hamesha ke liye yaad rakho.
            if guard.is_activated(chat_id):
                await message.reply(language.t(chat_id, "start_already_active"))
                return

            if not await guard.is_bot_admin(client, chat_id):
                await message.reply(language.t(chat_id, "start_needs_admin"))
                return

            await guard.activate(chat_id)
            await logger.log_new_group(client, message)

            buttons = build_start_menu_buttons(chat_id, client.me.username, in_group=True)
            await message.reply(
                language.t(chat_id, "start_group"),
                reply_markup=buttons,
            )

    @bot.on_message(filters.command("help"))
    async def help_cmd(client, message):
        chat_id = message.chat.id
        if not await fsub.check_subscription(client, message):
            return
        await message.reply(build_help_text(chat_id))

    @bot.on_message(filters.command("about"))
    async def about_cmd(client, message):
        chat_id = message.chat.id
        if not await fsub.check_subscription(client, message):
            return
        await message.reply(language.t(chat_id, "about_text", bot_name=config.BOT_NAME))

    @bot.on_callback_query(filters.regex(r"^show_about$"))
    async def about_callback(client, callback):
        chat_id = callback.message.chat.id
        await callback.message.reply(language.t(chat_id, "about_text", bot_name=config.BOT_NAME))
        await callback.answer()

    @bot.on_callback_query(filters.regex(r"^show_help$"))
    async def help_callback(client, callback):
        chat_id = callback.message.chat.id
        await callback.message.reply(build_help_text(chat_id))
        await callback.answer()

    @bot.on_callback_query(filters.regex(r"^show_lang_options$"))
    async def lang_callback(client, callback):
        chat_id = callback.message.chat.id
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇮🇳 Hindi", callback_data="setlang_hi"),
                InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en"),
            ]
        ])
        await callback.message.reply(language.t(chat_id, "lang_current"), reply_markup=buttons)
        await callback.answer()

    @bot.on_callback_query(filters.regex(r"^setlang_"))
    async def set_lang_callback(client, callback):
        chat_id = callback.message.chat.id
        lang_code = callback.data.split("_")[1]
        await language.set_lang(chat_id, lang_code)
        lang_name = "Hindi" if lang_code == "hi" else "English"
        await callback.message.edit(language.t(chat_id, "lang_set", lang_name=lang_name))
        await callback.answer()
