from pyrogram import filters

from Avenger import pbot as app
from Avenger.ex_plugins.dbfunctions import (
    antiservice_off,
    antiservice_on,
    is_antiservice_on,
)
from Avenger.utils.permissions import adminsOnly


@app.on_message(filters.command("antiservice") & ~filters.private)
@adminsOnly("can_change_info")
async def anti_service(_, message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ **Usage:** /antiservice <on / off>")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        await message.reply_text("**✅ ᴀɴᴛɪ ꜱᴇʀᴠɪᴄᴇ ᴛᴜʀɴ ᴏɴ**")
    elif status == "off":
        await message.reply_text("**❌ ᴀɴᴛɪ ꜱᴇʀᴠɪᴄᴇ ᴛᴜʀɴ ᴏꜰꜰ**")
    else:
        await message.reply_text("⚠️ **Usages :** /antiservice <on / off>")


@app.on_message(filters.service, group=11)
async def delete_service(_, message):
    chat_id = message.chat.id
    try:
        if await is_antiservice_on(chat_id):
            return await message.delete()
    except Exception:
        pass


__help__ = """
/antiservice <on / off>
*Note:* If on, The bot will auto delete service messages eg; user joined , user left etc.
"""
__mod_name__ = "A-ꜱᴇʀᴠɪᴄᴇ"
