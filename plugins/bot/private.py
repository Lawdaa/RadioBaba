"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from config import Config
from utils import USERNAME, mp
from pyrogram import Client, filters, emoji
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

msg=Config.msg
ADMINS=Config.ADMINS
CHAT_ID=Config.CHAT_ID
playlist=Config.playlist
LOG_GROUP=Config.LOG_GROUP

HOME_TEXT = "ðð» **Êá´Ê [{}](tg://user?id={})**,\n\nÉª'á´ **á´Êá´á´á´á´Êê± á´á´ê±Éªá´ Êá´á´Éªá´** \n**Éª á´á´É´ á´Êá´Ê 24/7 Êá´á´Éªá´ á´É´á´ ÊÉªá´ á´ ê±á´É´É¢ ê±á´Êá´á´á´ê± ê°Êá´á´ Êá´á´á´á´Êá´ ÉªÉ´** [á´Êá´á´á´á´Êê±ê±](https://t.me/chatterss) **ê±á´á´á´ÊÉ¢Êá´á´á´..!**\n\n**á´á´ê±ÉªÉ¢É´á´á´ ÊÊ :** [ðð¿ð²ð®ðð¼ð¿ ð£ð®ðð®ð»](https://t.me/itsCrePavan)"
HELP_TEXT = """
ð¡ --**Setting Up**--:

\u2022 Add the bot and user account in your group with admin rights.
\u2022 Start a voice chat in your group & restart the bot if not joined to vc.
\u2022 Use /play [song name] or use /play as a reply to an audio file or youtube link.

ð¡ --**Common Commands**--:

\u2022 `/help` - shows help for all commands
\u2022 `/song` [song name] - download the song as audio
\u2022 `/current` - shows current track with controls
\u2022 `/playlist` - shows the current & queued playlist

ð¡ --**Admins Commands**--:

\u2022 `/radio` - start radio stream
\u2022 `/stopradio` - stop radio stream
\u2022 `/skip` - skip current music
\u2022 `/join` - join the voice chat
\u2022 `/leave` - leave the voice chat
\u2022 `/stop` - stop playing music
\u2022 `/volume` - change volume (0-200)
\u2022 `/replay` - play from the beginning
\u2022 `/clean` - remove unused raw files
\u2022 `/pause` - pause playing music
\u2022 `/resume` - resume playing music
\u2022 `/mute` - mute the vc userbot
\u2022 `/unmute` - unmute the vc userbot
\u2022 `/restart` - update & restart the bot
\u2022 `/setvar` - set/change heroku configs

Â© **Powered By** : 
**@itsCrePavan | @Chatterss**
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "You're Not Allowed! ð¤£",
            show_alert=True
            )
        return

    if query.data.lower() == "replay":
        group_call = mp.group_call
        if not playlist:
            await query.answer("âï¸ Empty Playlist !", show_alert=True)
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("ð Replaying !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("ð", callback_data="replay"),
                                InlineKeyboardButton("â¸", callback_data="pause"),
                                InlineKeyboardButton("â©", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "pause":
        if not playlist:
            await query.answer("âï¸ Empty Playlist !", show_alert=True)
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("â¸ Paused !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("ð", callback_data="replay"),
                                InlineKeyboardButton("â¶ï¸", callback_data="resume"),
                                InlineKeyboardButton("â©", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "resume":   
        if not playlist:
            await query.answer("âï¸ Empty Playlist !", show_alert=True)
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("â¶ï¸ Resumed !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("ð", callback_data="replay"),
                                InlineKeyboardButton("â¸", callback_data="pause"),
                                InlineKeyboardButton("â©", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "skip":   
        if not playlist:
            await query.answer("âï¸ Empty Playlist !", show_alert=True)
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("â© Skipped !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("ð", callback_data="replay"),
                                InlineKeyboardButton("â¸", callback_data="pause"),
                                InlineKeyboardButton("â©", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "help":
        buttons = [
            [
                InlineKeyboardButton("Êá´Êá´ Éªê± á´ á´Êá´á´á´á´Ê", url="https://t.me/itsCrePavan"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "home":
        buttons = [
            [
                InlineKeyboardButton("Êá´Êá´ Éªê± á´ á´Êá´á´á´á´Ê", url="https://t.me/itsCrePavan"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass

    await query.answer()



@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("Êá´Êá´ Éªê± á´ á´Êá´á´á´á´Ê", url="https://t.me/itsCrePavan"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo="https://telegra.ph/file/89d4135199d1d2a98596e.jpg", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)


@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("Êá´Êá´ Éªê± á´ á´Êá´á´á´á´Ê", url="https://t.me/itsCrePavan"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_photo(photo="https://telegra.ph/file/89d4135199d1d2a98596e.jpg", caption=HELP_TEXT, reply_markup=reply_markup)
    await mp.delete(message)


@Client.on_message(filters.command(["setvar", f"setvar@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def set_heroku_var(client, message):
    if not Config.HEROKU_APP:
        buttons = [[InlineKeyboardButton('HEROKU_API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new')]]
        k=await message.reply_text(
            text="â **No Heroku App Found !** \n__Please Note That, This Command Needs The Following Heroku Vars To Be Set :__ \n\n1. `HEROKU_API_KEY` : Your heroku account api key.\n2. `HEROKU_APP_NAME` : Your heroku app name. \n\n**For More Ask In @AsmSupport !!**", 
            reply_markup=InlineKeyboardMarkup(buttons))
        await mp.delete(k)
        await mp.delete(message)
        return
    if " " in message.text:
        cmd, env = message.text.split(" ", 1)
        if  not "=" in env:
            k=await message.reply_text("â **You Should Specify The Value For Variable!** \n\nFor Example: \n`/setvar CHAT_ID=-1001313215676`")
            await mp.delete(k)
            await mp.delete(message)
            return
        var, value = env.split("=", 2)
        config = Config.HEROKU_APP.config()
        if not value:
            m=await message.reply_text(f"â **No Value Specified, So Deleting `{var}` Variable !**")
            await asyncio.sleep(2)
            if var in config:
                del config[var]
                await m.edit(f"ð **Sucessfully Deleted `{var}` !**")
                config[var] = None
            else:
                await m.edit(f"ð¤·ââï¸ **Variable Named `{var}` Not Found, Nothing Was Changed !**")
            return
        if var in config:
            m=await message.reply_text(f"â ï¸ **Variable Already Found, So Edited Value To `{value}` !**")
        else:
            m=await message.reply_text(f"â ï¸ **Variable Not Found, So Setting As New Var !**")
        await asyncio.sleep(2)
        await m.edit(f"â **Succesfully Set Variable `{var}` With Value `{value}`, Now Restarting To Apply Changes !**")
        config[var] = str(value)
        await mp.delete(m)
        await mp.delete(message)
        return
    else:
        k=await message.reply_text("â **You Haven't Provided Any Variable, You Should Follow The Correct Format..!** \n\nFor Example: \nâ¢ `/setvar CHAT_ID=-1001313215676` to change or set CHAT var. \nâ¢ `/setvar REPLY_MESSAGE=` to delete REPLY_MESSAGE var.")
        await mp.delete(k)
        await mp.delete(message)
