from Avenger.events import register
from Avenger import ubot2

@register(pattern="^/sg ?(.*)")
async def lastname(steal):
    steal.pattern_match.group(1)
    puki = await steal.reply("```Retrieving Such User Information..```")
    if steal.fwd_from:
        return
    if not steal.reply_to_msg_id:
        await puki.edit("```Please Reply To User Message.```")
        return
    message = await steal.get_reply_message()
    chat = "@SangMataInfo_bot"
    user_id = message.sender.id
    id = f"/search_id {user_id}"
    if message.sender.bot:
        await puki.edit("```Reply To Real User's Message.```")
        return
    await puki.edit("```Please wait...```")
    try:
        async with ubot2.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                r = await conv.get_response()
                response = await conv.get_response()
            if r.text.startswith("Name"):
                respond = await conv.get_response()
                await puki.edit(f"`{r.message}`")
                await ubot2.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id, respond.id]
                )
                return
            if response.text.startswith("No records") or r.text.startswith(
                "No records"
            ):
                await puki.edit(
                    "```I Can't Find This User's Information, This User Has Never Changed His Name Before.```"
                )
                await ubot2.delete_messages(conv.chat_id, [msg.id, r.id, response.id])
                return
            else:
                respond = await conv.get_response()
                await puki.edit(f"```{response.message}```")
            await ubot2.delete_messages(
                conv.chat_id, [msg.id, r.id, response.id, respond.id]
            )
