import os
import random
import glob
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterPhotos
from Avenger.events import register
from Avenger import telethn as tbot, ubot2
from telethon import events, Button, custom
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from Avenger import pbot
import requests
from pyrogram import Client, filters

BUTTON = [[Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", "https://t.me/AvengerBot?startgroup=true")]]
BUTTON += [[Button.url("ꜱᴜᴘᴘᴏʀᴛ", "https://t.me/BotsClubDiscussion"), Button.url("ᴜᴘᴅᴀᴛᴇꜱ", "https://t.me/BotsClubOfficial")]]

def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m


@register(pattern="^/logo ?(.*)")
async def logo_gen(event):
    xx = await event.reply("**ᴘʀᴇᴘᴀʀɪɴɢ ʟᴏɢᴏ**")
    name = event.pattern_match.group(1)
    if not name:
        await xx.edit("`Provide some text to draw!\nExample: /logo <your name>!`")
        return
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in ubot2.iter_messages(
            "@KenLogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
        fpath_ = glob.glob("./Avenger/resources/fonts/*")
        font_ = random.choice(fpath_)
    if not bg_:
        pics = []
        async for i in ubot2.iter_messages(
            "@KenLogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob.glob("./Avenger/resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 120
        strke = 10
    elif len(name) >= 9:
        fnt_size = 50
        strke = 5
    else:
        fnt_size = 100
        strke = 20
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text((x, y), name, font=font, fill="white",
              stroke_width=strke, stroke_fill="black")
    flnme = f"logo.png"
    img.save(flnme, "png")
    ii = await xx.edit("📩 **ᴜᴘʟᴏᴀᴅɪɴɢ**")
    if os.path.exists(flnme):
        await tbot.send_file(
            event.chat_id,
            file=flnme,
            caption="━━━━━━━  Aᴠᴇɴɢᴇʀ  ━━━━━━━\n\n☘️ ʟᴏɢᴏ ᴄʀᴇᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ☘️\n◈──────────────◈\n🔥 ᴄʀᴇᴀᴛᴇᴅ ʙʏ : [Aᴠᴇɴɢᴇʀ](https://t.me/AvengerBot)\n⚡️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [ʙᴏᴛꜱ ᴄʟᴜʙ](https://t.me/BotsClubOfficial)\n◈──────────────◈\n©2021 [ʙᴏᴛꜱ ᴄʟᴜʙ](https://t.me/BotsClubOfficial)™ ᴛᴇᴀᴍ\nʀᴇꜱᴇʀᴠᴇᴅ ᴀʟʟ ʀɪɢʜᴛ ⚠️️\n\n━━━━━━━  Aᴠᴇɴɢᴇʀ  ━━━━━━━", buttons=BUTTON,
            force_document=False,
        )
        os.remove(flnme)
        await ii.delete()
    if os.path.exists(bg_):
        os.remove(bg_) 
    if os.path.exists(font_):
        if not font_.startswith("./Avenger/resources/fonts"):
            os.remove(font_)


@register(pattern="^/wlogo ?(.*)")
async def logo_(event):
    xx = await event.reply("`Preparing your logo...`")
    name = event.pattern_match.group(1)
    if not name:
        await xx.edit("`Provide some text to draw!\nExample: /wlogo <your name>!`")
        return
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in ubot2.iter_messages(
            "@kenlogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
        fpath_ = glob.glob("./Avenger/resources/fonts/*")
        font_ = random.choice(fpath_)
    if not bg_:
        pics = []
        async for i in ubot2.iter_messages(
            "@kenlogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob.glob("./Avenger/resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 105
        strke = 8
    elif len(name) >= 9:
        fnt_size = 50
        strke = 4
    else:
        fnt_size = 95
        strke = 13
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text((x, y), name, font=font, fill="white",
              stroke_width=strke, stroke_fill="black")
    flnme = f"logo.png"
    img.save(flnme, "png")
    await xx.edit("`Uploading`")
    if os.path.exists(flnme):
        await tbot.send_file(
            event.chat_id,
            file=flnme,
            caption="━━━━━━━  Aᴠᴇɴɢᴇʀ  ━━━━━━━\n\n☘️ ʟᴏɢᴏ ᴄʀᴇᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ☘️\n◈──────────────◈\n🔥 ᴄʀᴇᴀᴛᴇᴅ ʙʏ : [Aᴠᴇɴɢᴇʀ](https://t.me/AvengerBot)\n⚡️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [ʙᴏᴛꜱ ᴄʟᴜʙ](https://t.me/BotsClubOfficial)\n◈──────────────◈\n©2021 [ʙᴏᴛꜱ ᴄʟᴜʙ](https://t.me/BotsClubOfficial)™ ᴛᴇᴀᴍ\nʀᴇꜱᴇʀᴠᴇᴅ ᴀʟʟ ʀɪɢʜᴛ ⚠️️\n\n━━━━━━━  Aᴠᴇɴɢᴇʀ  ━━━━━━━", buttons=BUTTON,
            force_document=False,
        )
        os.remove(flnme)
        await xx.delete()
    if os.path.exists(bg_):
        os.remove(bg_) 
    if os.path.exists(font_):
        if not font_.startswith("./Avenger/resources/fonts"):
            os.remove(font_)


@pbot.on_message(filters.command("picme"))
async def repolypj(_, message):
    id = message.from_user.photo.big_file_id
    m = await message.reply_text("📸 ᴄʀᴇᴀᴛɪɴɢ..")    
    photo = await pbot.download_media(id)
    caption = "━━━━━━━  Aᴠᴇɴɢᴇʀ  ━━━━━━━\n\n☘️ ᴛʜɪꜱ ɪꜱ ʏᴏᴜʀ ᴘʀᴏꜰɪʟᴇ ᴘɪᴄᴛᴜʀᴇ ☘️\n◈──────────────◈\n🔥 ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ : [Aᴠᴇɴɢᴇʀ](https://t.me/AvengerBot)\n⚡️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [ʙᴏᴛꜱ ᴄʟᴜʙ](https://t.me/BotsClubOfficial)\n◈──────────────◈\n©2021 [ʙᴏᴛꜱ ᴄʟᴜʙ](https://t.me/BotsClubOfficial)™ ᴛᴇᴀᴍ\nʀᴇꜱᴇʀᴠᴇᴅ ᴀʟʟ ʀɪɢʜᴛ ⚠️️\n\n━━━━━━━  Aᴠᴇɴɢᴇʀ  ━━━━━━━"
    pesan = await m.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ...")
    await pbot.send_chat_action(message.chat.id, "upload_photo")    
    await message.reply_photo(photo, caption)
    await pesan.delete()
    os.remove(photo)


__mod_name__ = "ʟᴏɢᴏ"

__help__ = """
*This is help menu for logomaker*
/logo <text/name> - Create a logo with random view.
/picme : Try as it is
"""
