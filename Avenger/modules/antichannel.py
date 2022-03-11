import asyncio
from Avenger import pbot
from pyrogram import filters
from Avenger.modules.helper_funcs.chat_status import adminsonly
from Avenger.modules.mongo.antichnl_mongo import (
    is_antichnl,
    antichnl_on,
    antichnl_off,
)


@pbot.on_message(filters.command("antichannel") & ~filters.channel)
@adminsonly
async def antic_toggle(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Use /antichannel with on or off")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    group_id = message.chat.id
    if status == "on":
        await antichnl_on(group_id, "low")
        await message.reply_text("✅ **ᴀɴᴛɪᴄʜᴀɴɴᴇʟ ᴇɴᴀʙʟᴇᴅ** ✅")
    elif status == "low":
        await antichnl_on(group_id, "low")
        await message.reply_text("Antichannel enabled.")
    elif status == "high":
        await antichnl_on(group_id, "low")
        await message.reply_text(
            "Antichannel enabled, High mode is not currently working, So enabled low mode."
        )
    elif status == "off":
        await antichnl_off(group_id)
        await message.reply_text("❌ **ᴀɴᴛɪᴄʜᴀɴɴᴇʟ ᴅɪꜱᴀʙʟᴇᴅ** ❌")
    else:
        await message.reply_text("Use /antichannel with on or off")


@pbot.on_message(filters.text & ~filters.linked_channel, group=36)
async def anitchnl(_, message):
    chat_id = message.chat.id
    if message.sender_chat:
        sender = message.sender_chat.id
        isantichl, mode = await is_antichnl(chat_id)
        if not isantichl:
            return
        if chat_id == sender:
            return
        else:
            await message.delete()


__help__ = """
*ANTI-CHANNEL MODULE*
/antichannel on : Turn On Antichannel Function
/antichannel off : Turn Off Antichannel Function
"""

__mod_name__ = "A-ᴄʜᴀɴɴᴇʟ"
