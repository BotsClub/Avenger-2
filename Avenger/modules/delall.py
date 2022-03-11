import asyncio
import time

from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins

from Avenger import DEV_USERS, telethn
from Avenger.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)


async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in DEV_USERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern="^[!/]delall$"))
async def delall(event):
    chat = event.chat_id
    start = time.perf_counter()
    msgs = []

    if not await is_administrator(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("You're Not An Admin!")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await event.client.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []

        await event.client.delete_messages(chat, msgs)
        time_ = time.perf_counter() - start
        del_res = await event.client.send_message(
            event.chat_id, f"✅ ᴅᴇʟᴇᴛᴇᴅ {count} ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ {time_:0.2f} ꜱᴇᴄᴏɴᴅꜱ"
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "Failed to delete messages.\n"
        text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
        del_res = await event.respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


__help__ = """
*Admins Only Command*
/delall : Reply with message from where all messages should be deleted
*NOTE: Purge can only delete messages sent with 24 hours and purge can only delete 100 messages in single time but /delall can delete whole messages from the starting*
"""
__mod_name__ = "Dᴇʟᴀʟʟ"
