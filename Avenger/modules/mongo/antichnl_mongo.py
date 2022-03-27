from Avenger import db
from typing import Dict, List, Union

anitcdb = db.antichnl

async def is_antichnl(group_id):
    data = await anitcdb.find_one({"group_id": group_id})
    if not data:
        return False, None
    else:
        return True, data["mode"]


async def antichnl_on(group_id, mode):
    data = {"group_id": group_id, "mode": (mode)}
    try:
        anitcdb.update_one({"group_id": group_id}, {"$set": data}, upsert=True)
    except:
        return


async def antichnl_off(group_id):
    is_captcha, type = await is_antichnl(group_id)
    if not is_captcha:
        return
    return anitcdb.delete_one({"group_id": group_id})
