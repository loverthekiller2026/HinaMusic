#
# Copyright (C) 2021-2022 by TheAloneteam@Github, < https://github.com/TheAloneTeam >.
# This file is part of < https://github.com/TheAloneTeam/AloneMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheAloneTeam/AloneMusic/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import random
import time
from io import BytesIO
from urllib.request import Request, urlopen

from py_yt import VideosSearch
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (ChatAdminRequired, InviteRequestSent,
                             UserAlreadyParticipant)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from AloneMusic import app
from AloneMusic.misc import _boot_
from AloneMusic.plugins.sudo.sudoers import sudoers_list
from AloneMusic.utils.database import (add_served_chat, add_served_user,
                                       blacklisted_chats, get_assistant,
                                       get_lang, is_banned_user, is_on_off)
from AloneMusic.utils.decorators.language import LanguageStart
from AloneMusic.utils.formatters import get_readable_time
from AloneMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string



_START_PHOTO_CACHE = None


def _download_start_photo(url):
    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; HinaMusic/1.0)"},
    )
    with urlopen(request, timeout=20) as response:
        image = response.read(10 * 1024 * 1024 + 1)
        if len(image) > 10 * 1024 * 1024:
            raise ValueError("Start image is larger than 10 MB")
        if not image.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"GIF8", b"RIFF")):
            raise ValueError("START_IMG_URL did not return a valid image")
        return image


async def send_start_photo(message, caption, reply_markup, **kwargs):
    """Send the configured start image as an upload, with a text fallback."""
    global _START_PHOTO_CACHE
    try:
        if _START_PHOTO_CACHE is None:
            _START_PHOTO_CACHE = await asyncio.to_thread(
                _download_start_photo, config.START_IMG_URL
            )
        photo = BytesIO(_START_PHOTO_CACHE)
        photo.name = "hinamusic-start.jpg"
        await message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=reply_markup,
            **kwargs,
        )
    except Exception as exc:
        print(f"[START] Photo send failed; using text fallback: {exc}")
        await message.reply_text(
            caption,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )


EFFECT_ID = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.react("🍓", big=True)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await send_start_photo(
                message,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
                has_spoiler=True,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                has_spoiler=True,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        await send_start_photo(
            message,
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
            has_spoiler=True,
            message_effect_id=random.choice(EFFECT_ID),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await send_start_photo(
        message,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
        has_spoiler=True,
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await send_start_photo(
                    message,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                    has_spoiler=True,
                )
                await add_served_chat(message.chat.id)
                userbot = await get_assistant(message.chat.id)
                myu = await message.reply_text(_["call_4"].format(app.mention))
                try:
                    try:
                        get = await app.get_chat_member(message.chat.id, userbot.id)
                    except ChatAdminRequired:
                        return
                    if (
                        get.status == ChatMemberStatus.BANNED
                        or get.status == ChatMemberStatus.RESTRICTED
                    ):
                        try:
                            await app.unban_chat_member(message.chat.id, userbot.id)
                        except:
                            return
                except:
                    pass

                if message.chat.username:
                    invitelink = message.chat.username
                    try:
                        await userbot.resolve_peer(invitelink)
                    except:
                        pass
                else:
                    try:
                        invitelink = await app.export_chat_invite_link(message.chat.id)
                    except:
                        return

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                try:
                    await asyncio.sleep(1)
                    await userbot.join_chat(invitelink)
                    await myu.edit(_["call_5"].format(app.mention))
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(
                            message.chat.id, userbot.id
                        )
                    except:
                        return
                except UserAlreadyParticipant:
                    pass
                except:
                    return

                try:
                    await userbot.resolve_peer(message.chat.id)
                except:
                    pass

                await message.stop_propagation()
        except Exception as ex:
            print(ex)
