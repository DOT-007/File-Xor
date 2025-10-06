from pyrogram import Client, filters
from pyrogram.types import Message
from file_xor.database.Usr_detailBan_db import db, ensure_db_ready
from file_xor import roxe
from config import BotInfoConfig
from file_xor.lang import msg_translate, lang

@roxe.on_message(filters.command("ban")& filters.user(BotInfoConfig.SUDO))
async def ban_user(client: Client, message: Message):
    await ensure_db_ready()
    if len(message.command) < 2:
        return await message.reply("Usage: `/ban <user_id> [reason]`", quote=True)
    
    user_id = int(message.command[1])
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else None
    await db.add_ban(user_id, reason)
    await message.reply(msg_translate(lang, "BanNotification"))

@roxe.on_message(filters.command("unban")& filters.user(BotInfoConfig.SUDO))
async def unban_user(client: Client, message: Message):
    await ensure_db_ready()
    if len(message.command) < 2:
        return await message.reply("Usage: `/unban <user_id>`", quote=True)
    
    user_id = int(message.command[1])
    await db.remove_ban(user_id)
    await message.reply(msg_translate(lang, "UnbanNotification"))


@roxe.on_message(filters.command("viewbans")& filters.user(BotInfoConfig.SUDO))
async def view_bans(client: Client, message: Message):
    await ensure_db_ready()
    bans = await db.get_bans()
    if not bans:
        return await message.reply(msg_translate(lang, "NoBannedUsers"))
    
    text = "**Banned Users:**\n\n"
    for uid, reason, ts in bans:
        text += f"**User ID:** `{uid}`\n**Reason:** `{reason or 'None'}`\n**At:** `{ts}`\n\n"
    
    await message.reply(text)

