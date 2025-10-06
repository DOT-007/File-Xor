# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from config import BotInfoConfig 
from pyrogram import filters
from file_xor import roxe
import asyncio
from file_xor.lib.reboot_backend import restart_process, graceful_shutdown
from file_xor.lang import msg_translate , lang



# Define the command for rebooting the bot
@roxe.on_message(filters.command("reboot") & filters.user(BotInfoConfig.SUDO))
async def reboot_bot(client, message):
    await message.react("🦄")
    await message.reply_text(msg_translate(lang, "RebootNofication"))
    restart_process()


# Command for shutting down the bot
@roxe.on_message(filters.command("shutdown") & filters.user(BotInfoConfig.SUDO))
async def shutdown_bot(client, message):
    await message.reply_text(msg_translate(lang, "ShutDownPrevent"))
    countdown = 5
    countdown_message = await message.reply_text(msg_translate(lang, "ShutDownCountBegins"))

    for i in range(countdown, 0, -1):
        # format the countdown message with the remaining seconds
        await countdown_message.edit_text(msg_translate(lang, "ShutDownCountBegins2").format(i=i))
        await asyncio.sleep(1)

    await message.reply_text(msg_translate(lang, "GoodByeMsg"))
    await graceful_shutdown(roxe)
