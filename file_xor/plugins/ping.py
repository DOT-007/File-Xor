import time
from file_xor import roxe
from pyrogram import filters
from pyrogram.types import Message
from file_xor.lib.ping_backend import calc_response_time_ms
from file_xor.lib.isVerify import isPrivate , isBanned


@roxe.on_message(filters.command("ping"))
@isPrivate
@isBanned
async def ping_command(app, message: Message):
    start_time = time.time()
    reply = await message.reply_text("Pinging...")
    end_time = time.time()
    response_time = calc_response_time_ms(start_time, end_time)
    pingmsg = f"Response time: {response_time} ms"
    await reply.edit_text(pingmsg)


