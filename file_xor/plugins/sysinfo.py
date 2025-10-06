from pyrogram import filters
from file_xor import roxe
from config import BotInfoConfig
from file_xor.lib.sysinfo_backend import format_system_info
from file_xor.lib.isVerify import isPrivate , isBanned

# This command will show the system information of the bot
@roxe.on_message(filters.command("sysinfo"))
@isPrivate
@isBanned
async def send_system_info(client, message):
    info = format_system_info(BotInfoConfig.BOT_NAME)
    await message.reply(info)

