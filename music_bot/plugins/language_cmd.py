from pyrogram import filters
import language
import fsub


def register(bot, call_py):

    @bot.on_message(filters.command("language") & filters.group)
    async def language_cmd(client, message):
        chat_id = message.chat.id
        if not await fsub.check_subscription(client, message):
            return

        if len(message.command) < 2:
            await message.reply(language.t(chat_id, "lang_current"))
            return

        choice = message.command[1].lower()

        if choice in ("hindi", "hi"):
            await language.set_lang(chat_id, "hi")
            await message.reply(language.t(chat_id, "lang_set", lang_name="Hindi"))
        elif choice in ("english", "en"):
            await language.set_lang(chat_id, "en")
            await message.reply(language.t(chat_id, "lang_set", lang_name="English"))
        else:
            await message.reply(language.t(chat_id, "lang_invalid"))
