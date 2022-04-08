from pyrogram.errors import InputUserDeactivated,FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram import Client, filters
import datetime
import time
import asyncio
from pyrogram import filters
from Avenger import *
from Avenger import DEV_USERS
from Avenger.modules.no_sql.users_db import get_all_chats, get_all_users
from pyrogram import __version__ as pyrover
import asyncio
import platform
import time
from datetime import datetime
from sys import version as pyver
import psutil
from pymongo import MongoClient
from pyrogram import Client
from pyrogram import filters
import speedtest
import wget
import os
import sys
from Avenger.modules.no_sql import users_db as db
from git import Repo
from os import system, execle, environ
from git.exc import InvalidGitRepositoryError
from pyrogram.types import Message
from pyrogram import Client, filters


@Client.on_message(filters.command("bcast") & filters.user(DEV_USERS) & filters.reply)
async def bcast(bot, message):
    served_users = len(await get_all_users())
    served_users = []
    users = await get_all_users()
    for user in users:
        served_users.append(int(user["user_id"]))
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your message...'
    )
    start_time = time.time()
    total_users = await db.num_users()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f">>>  Broadcast in progress:\n\n •Total Users `{total_users}` \n •Completed: `{done}` / **{total_users}**\n •Success: `{success}`\n •Blocked: {blocked}\n • Deleted: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f" >>> Broadcast Completed:\n •Completed in {time_taken} seconds.\n\n •Total Users {total_users}\n •Completed: {done} / {total_users}\n •Success: {success}\n •Blocked: {blocked}\n •Deleted: {deleted}")

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        return False, "Error"
