# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from file_xor import roxe
from config import BotInfoConfig
from pyrogram import filters
from file_xor.lib.status_backend import get_system_stats
from file_xor.lib.isVerify import isPrivate , isBanned

# Stats command to get system stats
@roxe.on_message(filters.command("stats"))
@isPrivate
@isBanned
async def stats(client, message):
    response = get_system_stats(BotInfoConfig.BOT_NAME)
    await message.reply_text(response)



