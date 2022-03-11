import random

from telegram import ParseMode
from telethon import Button

from Executive import OWNER_ID, SUPPORT_CHAT
from Executive import telethn as tbot

from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    NATSUNAGI = (
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
        "https://telegra.ph/file/3eb2282a7c4df03a4c61e.jpg",
    )
    NATFEED = ("https://telegra.ph/file/2dd04f407b16bc2cfdf76.jpg",)
    BUTTON = [[Button.url("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", f"https://t.me/ExecutiveRobot?startgroup=new")]]
    TEXT = "**ᴛʜᴀɴᴋꜱ** ꜰᴏʀ ʏᴏᴜʀ **ꜰᴇᴇᴅʙᴀᴄᴋ**, ɪ ʜᴏᴘᴇ ʏᴏᴜ ᴀʀᴇ **ʜᴀᴘᴘʏ ᴡɪᴛʜ ᴏᴜʀ ꜱᴇʀᴠɪᴄᴇ**"
    GIVE = "Give Some Text For Feedback ✨"
    logger_text = f"""
**New Feedback**
**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(NATFEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(NATSUNAGI),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(NATSUNAGI), buttons=BUTTON)

__help__ = """
/feedback <Your Feedback message here> 
*Note:* No need to send message to bot owner directly, you can give him feedback about hist bot via this amazing plugin.
"""
__mod_name__ = "ꜰᴇᴇᴅʙᴀᴄᴋ"
