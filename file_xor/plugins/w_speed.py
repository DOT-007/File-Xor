import speedtest
from file_xor import roxe
from pyrogram import filters
from config import BotInfoConfig
from file_xor.lang import msg_translate
from file_xor.lib.isVerify import isPrivate , isBanned

@roxe.on_message(filters.command("speedtest"))
@isPrivate
@isBanned
async def speedtest_handler(client, message):
    lang = BotInfoConfig.LANG
    msg = await message.reply_text(msg_translate(lang, "SpeedTestBegins"))

    try:
        st = speedtest.Speedtest()
        st.get_best_server()   # finds best server
        download_speed = st.download()
        upload_speed = st.upload()
        ping = st.results.ping

        # Convert bits/s to Mbps
        download_mbps = round(download_speed / 1_000_000, 2)
        upload_mbps = round(upload_speed / 1_000_000, 2)

        result_text = (
            f"✅ " + msg_translate(lang, "SpeedTestBegins") + "\n\n"
            f"📶 Download: {download_mbps} Mbps\n"
            f"📤 Upload: {upload_mbps} Mbps\n"
            f"⏱️ Ping: {ping} ms"
        )

        await msg.edit_text(result_text)

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")