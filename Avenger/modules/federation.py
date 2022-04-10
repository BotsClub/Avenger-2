import html
import time
import uuid
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup)
from Avenger import BOT_ID, TELEGRAM_SERVICES_IDs, JOIN_LOGGER as LOG_CHANNEL, pbot
from Avenger.helper import custom_filter
from Avenger.helper.get_user import get_user_id
from Avenger.helper.chat_status import isUserCreator, isBotCan
from Avenger.modules.mongo.federation_mongo import (get_connected_chats,
                                              get_fed_admins,
                                              get_fed_from_chat, get_fed_name,
                                              get_fed_reason, is_user_fban,
                                              update_reason, user_fban, user_unfban,
                                              fed_promote, get_fed_from_ownerid, new_fed_db,
                                              fed_rename_db, is_fed_exist, join_fed_db)


@pbot.on_message(filters.all & filters.group, group=2)
async def fed_checker(client, message):
    
    chat_id = message.chat.id
    
    if not message.from_user:
        return

    user_id = message.from_user.id 
    fed_id = get_fed_from_chat(chat_id)
    
    if not fed_id == None:
        if is_user_fban(fed_id, user_id):
            fed_reason = get_fed_reason(fed_id, user_id)
            text = (
                    "**This user is banned in the current federation:**\n\n"
                    f"User: {message.from_user.mention} (`{message.from_user.id}`)\n"
                    f"Reason: `{fed_reason}`"
                )
            if await isBotCan(message, permissions='can_restrict_members'):
                if await pbot.kick_chat_member(chat_id, user_id): 
                    text += '\nAction: `Banned`'
            
            await message.reply(
                text
            )
            return

@pbot.on_message(custom_filter.command(commands=('fban')))
async def fed_ban(client, message):
    chat_id = message.chat.id
    user_info = await get_user_id(message)
    userID = user_info.id 
    
    bannerMention = message.from_user.mention 
    banner_name = message.from_user.first_name
    bannedID = message.from_user.id

    fed_id = get_fed_from_chat(chat_id)
    fed_name = get_fed_name(fed_id=fed_id)
    get_user = await StellaCli.get_users(
                user_ids=userID
            )

    FED_ADMINS = get_fed_admins(fed_id)
    
    if userID == BOT_ID:
        await message.reply(
            "Hahahaha no. I am not going to fban myself."
        )
        return
    
    if bannedID not in FED_ADMINS:
        await message.reply(
            f"You aren't a federation admin of {fed_name}."
        )
        return

    if (
        message.reply_to_message 
        and len(message.command) >= 2
    ):
        reason_text = ' '.join(message.text.split()[1:])   
    
    elif (
        len(message.command) >= 3
    ):
        reason_text = ' '.join(message.text.split()[2:])  

    else:
        reason_text = 'No reason was given'
     
    
    reason = f"{reason_text} // Fbanned by {banner_name} id {bannedID}"
    if is_user_fban(fed_id, userID):
        old_reason = get_fed_reason(fed_id, userID)
        if not old_reason == reason:
            update_reason(fed_id, userID, reason)
            fed_message = (
            f'**This user was already banned in the** "{fed_name}" **federation, I\'ll update the reason:**\n\n'
            f"Fed Administrator: {bannerMention}\n"
            f"User: {get_user.mention}\n"
            f"User ID: `{userID}`\n"
            f"Old Reason: `{old_reason}`\n"
            f"Updated Reason: `{reason}`"
        )
        else:
            fed_message = (
                f"User {get_user.mention} has already been fbanned, with the exact same reason."
            )
    else:
        user_fban(fed_id, userID, reason)
        connected_chats = get_connected_chats(fed_id)
        BannedChats = []
        for chat_id in connected_chats:
            GetData = await pbot.get_chat_member(
                chat_id=chat_id,
                user_id=BOT_ID
            )
            if GetData['can_restrict_members']:
                if await pbot.kick_chat_member(
                    chat_id,
                    userID
                ):
                    BannedChats.append(chat_id)
            else:
                continue

        fed_message = (
                f'**New Federation Ban in the** "{fed_name}" **federation:**\n\n'
                f"Fed Administrator: {bannerMention}\n"
                f"User: {get_user.mention}\n"
                f"User ID: `{userID}`\n"
                f"Reason: {reason}\n"
                f"Affected Chats: `{len(BannedChats)}`"
            )

    await message.reply(
        fed_message
    )

@pbot.on_message(custom_filter.command(commands=('unfban')))
async def unfed_ban(client, message):
    chat_id = message.chat.id
    user_info = await get_user_id(message)
    userID = user_info.id 
    
    bannerMention = message.from_user.mention 
    banner_name = message.from_user.first_name
    bannedID = message.from_user.id

    fed_id = get_fed_from_chat(chat_id)
    fed_name = get_fed_name(fed_id=fed_id)
    get_user = await pbot.get_users(
                user_ids=userID
            )

    FED_ADMINS = get_fed_admins(fed_id)
    
    if userID == BOT_ID:
        await message.reply(
             "How do you think I would've fbanned myself that you are trying to unfban me? Never seen such retardedness ever before."
        )
        return
    
    if bannedID not in FED_ADMINS:
        await message.reply(
            f"You aren't a federation admin of {fed_name}."
        )
        return

    if (
        message.reply_to_message 
        and len(message.command) >= 2
    ):
        reason_text = ' '.join(message.text.split()[1:])   
    
    elif (
        len(message.command) >= 3
    ):
        reason_text = ' '.join(message.text.split()[2:])  

    else:
        reason_text = 'No reason was given'
     
    
    reason = f"{reason_text} // un-Fbanned by {banner_name} id {bannedID}"
    if is_user_fban(fed_id, userID):
        user_unfban(fed_id, userID)
    else:
        pass

@pbot.on_message(custom_filter.command(commands=('fedpromote')))
async def FedPromote(client, message):
    user_info = await get_user_id(message)
    user_id = user_info.id 
    
    owner_id = message.from_user.id 
    fed_id = get_fed_from_ownerid(owner_id)
    fed_name = get_fed_name(owner_id=owner_id)
    user = await pbot.get_users(
        user_ids=user_id
    )

    if (
        message.chat.type == 'private'
    ):
        await message.reply(
            "This command is made to be run in a group where the person you would like to promote is present."
        )
        return
    
    if (
        fed_id == None
    ):
        await message.reply(
            "Only federation creators can promote people, and you don't even seem to have a federation to promote to!"
        )
        return
    
    if (
        is_user_fban(fed_id, user_id)
    ):
        await message.reply(
            f"User {user.mention} is fbanned in {fed_name}. You have to unfban them before promoting."
        )
        return

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text='Confirm', callback_data=f'fedpromote_promote_{user_id}_{owner_id}'),
                    InlineKeyboardButton(text='Cancel', callback_data=f'fedpromote_cancel_{user_id}_{owner_id}')
                ]
            ]
        )

    await message.reply(
        f"Please get {user.mention} to confirm that they would like to be fed admin for {fed_name}.",
        reply_markup=keyboard
    )


@pbot.on_callback_query(filters.create(lambda _, __, query: 'fedpromote_' in query.data))
async def fedpromote_callback(client: pbot, callback_query: CallbackQuery):
    
    query_data = callback_query.data.split('_')[1]
    user_id = int(callback_query.data.split('_')[2])
    owner_id = int(callback_query.data.split('_')[3])
    fed_id = get_fed_from_ownerid(owner_id)
    fed_name = get_fed_name(owner_id=owner_id)
    user = await pbot.get_users(
        user_ids=user_id
    )
    owner = await pbot.get_users(
        user_ids=owner_id
    )

    if query_data == 'promote':
        if user_id == callback_query.from_user.id:
            fed_promote(fed_id, user_id)
            await callback_query.edit_message_text(
                text=(
                    f"User {user.mention} is now admin of {fed_name} ({fed_id})"
                )
            )
        else:
            await callback_query.answer(
                text=(
                    "You aren't the user being promoted."
                )
            )

    elif query_data == 'cancel':
        if user_id == callback_query.from_user.id:
            await callback_query.edit_message_text(
                text=(
                    f"Fedadmin promotion has been refused by {user.mention}."
                )
            )

        elif owner_id == callback_query.from_user.id:
            await callback_query.edit_message_text(
                text=(
                    f"Fedadmin promotion cancelled by {owner.mention}."
                )
            )
        else:
            await callback_query.answer(
                text=(
                    "You aren't the user being promoted."
                )
            )

@pbot.on_message(custom_filter.command(commands=('newfed')))
async def NewFed(client, message):

    if (
        message.chat.type == 'supergroup'
    ):
        await message.reply(
            'Create your federation in my PM - not in a group.'
        )
        return 

    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "Give your federation a name!"
        )  
        return

    if (
        message.from_user.id in TELEGRAM_SERVICES_IDs
    ):
        await message.reply(
            "This is telegram services IDs, I should not create any new fed for it."
        )
        return

    if (
        len(' '.join(message.command[1:])) > 60
    ):
        await message.reply(
            "Your fed must be smaller than 60 words."
        )
        return

    fed_name = ' '.join(message.command[1:])
    fed_id = str(uuid.uuid4())
    owner_id = message.from_user.id 
    created_time = time.ctime() 

    new_fed_db(fed_name, fed_id, created_time, owner_id)

    await message.reply(
        (
            "Created new federation with FedID: "
            f"`{fed_id}`\n\n"
            "Use this ID to join federation! eg:\n"
            f"`/joinfed {fed_id}`"
        )
    )

    await pbot.send_message(
        chat_id=LOG_CHANNEL,
        text=(
            "New Federation created with FedID: "
            f"`{fed_id}`\n"
            f"OwnerID: `{owner_id}`\n"
            f"Created at `{created_time}`"
        )
    )

@pbot.on_message(custom_filter.command(commands=('renamefed')))
async def Rename_fed(client, message):
    owner_id = message.from_user.id 

    if not (
        message.chat.type == 'private'
    ):
        await message.reply(
            "You can only rename your fed in PM."
        )
        return

    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "You need to give your federation a name! Federation names can be up to 64 characters long."
        )
        return
    
    if (
        len(' '.join(message.command[1:])) > 60
    ):
        await message.reply(
            "Your fed must be smaller than 60 words."
        )
        return

    fed_id = get_fed_from_ownerid(owner_id)
    if fed_id == None:
        await message.reply(
            "It doesn't look like you have a federation yet!"
        )
        return
    
    fed_name = ' '.join(message.command[1:])
    old_fed_name = get_fed_name(owner_id=owner_id)
    

    fed_rename_db(owner_id, fed_name)
    await message.reply(
        f"I've renamed your federation from '{old_fed_name}' to '{fed_name}'. ( FedID: `{fed_id}`.)"
    )

    # Send notification of Rename Fed to the all connected chat

    connected_chats = get_connected_chats(fed_id)
    for chat_id in connected_chats:
        await pbot.send_message(
            chat_id=chat_id,
            text=(
                "**Federation renamed**\n"
                f"**Old fed name:** {old_fed_name}\n"
                f"**New fed name:** {fed_name}\n"
                f"FedID: `{fed_id}`"
            )
        )

@pbot.on_message(custom_filter.command(commands=('joinfed')))
async def JoinFeb(client, message):
    
    if not (
        message.chat.type == 'supergroup'
    ):
        await message.reply(
            "Only supergroups can join feds."
        )
        return 
    
    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "You need to specify which federation you're asking about by giving me a FedID!"
        )
        return

    if not (
        await isUserCreator(message)
    ):
        await message.reply(
            "Only Group Creator can join new fed!"
        )
        return 

    if not (
        is_fed_exist(message.command[1])
    ):
        await message.reply(
            "This FedID does not refer to an existing federation."
        )
        return

    fed_id = message.command[1]
    chat_id = message.chat.id
    chat_title = html.escape(message.chat.title)
    fed_name = get_fed_name(fed_id)

    join_fed_db(chat_id, chat_title,  fed_id)
    await message.reply(
        f'Successfully joined the "{fed_name}" federation! All new federation bans will now also remove the members from this chat.'
    )


__help__ = """
**Commands:**
/fban: Bans a user from the current chat's federation
/unfban: Unbans a user from the current chat's federation
/feddemoteme `<fedID>`: Demote yourself from a fed.
/myfeds: List all feds you are an admin in.
/fedinfo `<FedID>`: Information about a federation.
/fedadmins `<FedID>`: List the admins in a federation.
/fedsubs `<FedID>`: List all federations your federation is subscribed to.
/joinfed `<FedID>`: Join the current chat to a federation. A chat can only join one federation. Chat owners only.
/leavefed: Leave the current federation. Only chat owners can do this.
/fedstat: List all the federations you are banned in.
/fedstat `<user ID>`: List all the federations a user has been banned in.
/fedstat `<user ID> <FedID>`: Gives information about a user's ban in a federation.
/chatfed: Information about the federation the current chat is in.
/quietfed `<yes/no/on/off>`: Whether or not to send ban notifications when fedbanned users join the chat.
**Owner Commands:**
/newfed `<fedname>`: Creates a new federation with the given name. Only one federation per user.
/renamefed `<fedname>`: Rename your federation.
/delfed: Deletes your federation, and any information related to it. Will not unban any banned users.
/fedtransfer `<reply/username/mention/userid>`: Transfer your federation to another user.
/fedpromote: Promote a user to fedadmin in your fed. To avoid unwanted fedadmin, the user will get a message to confirm this.
/feddemote: Demote a federation admin in your fed.
/fednotif `<yes/no/on/off>`: Whether or not to receive PM notifications of every fed action.
/fedreason `<yes/no/on/off>`: Whether or not fedbans should require a reason.
/subfed `<FedId>`: Subscribe your federation to another. Users banned in the subscribed fed will also be banned in this one.
Note: This does not affect your banlist. You just inherit any bans.
/unsubfed `<FedId>`: Unsubscribes your federation from another. Bans from the other fed will no longer take effect.
/fedexport `<csv/minicsv/json/human>`: Get the list of currently banned users. Default output is CSV.
/fedimport: Import a list of banned users.
/setfedlog: Sets the current chat as the federation log. All federation events will be logged here.
/unsetfedlog: Unset the federation log. Events will no longer be logged.
"""

__mod_name__ = "Fᴇᴅᴇʀᴀᴛɪᴏɴ"
