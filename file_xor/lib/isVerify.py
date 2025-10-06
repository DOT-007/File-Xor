from functools import wraps
from pyrogram import Client, filters
from pyrogram.types import Message  
from config import BotInfoConfig
from file_xor.database.Usr_detailBan_db import db, ensure_db_ready
from file_xor.lang import msg_translate
lang = BotInfoConfig.LANG

PrivateTextMsg = msg_translate(lang, "PrivateTextMsg")
BannedTextMsg = msg_translate(lang, "BannedTextMsg")
# ------------------------------
# Private mode decorator
# ------------------------------
def is_admin(user_id: int) -> bool:
    return user_id in BotInfoConfig.SUDO

# ------------------------------
# Check if a user is banned
# ------------------------------
async def is_banned(user_id: int) -> bool:
    # Ensure DB initialization completed (if scheduled on the running loop)
    try:
        await ensure_db_ready()
    except Exception:
        # If waiting fails for some reason, continue and let the subsequent
        # attribute access raise a clearer exception for troubleshooting.
        pass
    
    if db.pg_pool:
        async with db.pg_pool.acquire() as conn:
            row = await conn.fetchrow("SELECT 1 FROM bans WHERE user_id = $1", user_id)
            return bool(row)
    else:
        cur = db.sqlite_conn.cursor()
        cur.execute("SELECT 1 FROM bans WHERE user_id = ?", (user_id,))
        return bool(cur.fetchone())


def isPrivate(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if BotInfoConfig.MODE.lower() == "public" or is_admin(message.from_user.id):
            return await func(client, message)
        await message.reply(PrivateTextMsg)
    return wrapper

def isBanned(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if await is_banned(user_id):
            return await message.reply(BannedTextMsg)
        return await func(client, message)
    return wrapper


def sudo_filter(_, __, message):
    return message.from_user and message.from_user.id in BotInfoConfig.SUDO

sudo = filters.create(sudo_filter)
