from telethon import custom, events, Button
import os, re
from Executive import telethn as bot
from Executive import telethn as tgbot
from Executive.events import register


@register(pattern="/myinfo")
async def proboyx(event):
    button = [[custom.Button.inline("ʏᴏᴜʀ ᴅᴇᴛᴀɪʟꜱ", data="information")]]
    await bot.send_message(event.chat, "YOUR INFORMATION", buttons=button)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
    try:
        boy = event.sender_id
        PRO = await bot.get_entity(boy)
        EXECUTIVE = "**ʏᴏᴜʀ ᴅᴇᴛᴀɪʟꜱ ʙʏ ᴇxᴇᴄᴜᴛɪᴠᴇ**\n"
        EXECUTIVE += f"**ꜰɪʀꜱᴛ ɴᴀᴍᴇ :** {PRO.first_name} \n"
        EXECUTIVE += f"**ʟᴀꜱᴛ ɴᴀᴍᴇ :** {PRO.last_name}\n"
        EXECUTIVE += f"**ʏᴏᴜ ʙᴏᴛ :** {PRO.bot} \n"
        EXECUTIVE += f"**ʀᴇꜱᴛʀɪᴄᴛᴇᴅ :** {PRO.restricted} \n"
        EXECUTIVE += f"**ᴜꜱᴇʀ ɪᴅ :** {boy}\n"
        EXECUTIVE += f"**ᴜꜱᴇʀɴᴀᴍᴇ :** @{PRO.username}\n"
        await event.answer(EXECUTIVE, alert=True)
    except Exception as e:
        await event.reply(f"{e}")
