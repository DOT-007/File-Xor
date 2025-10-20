from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
import logging
from file_xor.lib.url_utils import normalize_base_url, is_valid_http_url
from file_xor.lib.button_builder import build_button_row
from secrets import token_hex
from file_xor import roxe
from config import TgConfig, ServerConfig
from file_xor.lang import msg_translate , lang
from file_xor.lib.isVerify import isBanned

@roxe.on_message(filters.document | filters.video | filters.video_note | filters.audio | filters.voice | filters.photo)
@isBanned
async def handle_user_file(_, msg: Message):
    # allow private chats, groups and supergroups
    if msg.chat.type not in ("private", "group", "supergroup"):
        return

    # get sender id more robustly (channels/anonymous admins may not have from_user)
    if getattr(msg, "from_user", None) and msg.from_user:
        sender_id = msg.from_user.id
    elif getattr(msg, "sender_chat", None) and msg.sender_chat:
        sender_id = msg.sender_chat.id
    else:
        sender_id = msg.chat.id

    secret_code = token_hex(ServerConfig.GEN_SECRET_KEY_LENGTH)

    try:
        file = await msg.copy(
            chat_id=TgConfig.FILEDB_CHANNEL,
            caption=f"||sender_id={sender_id},\n secret_code={secret_code}||"
        )
    except Exception as e:
        return await msg.reply(f"❌ Failed to store file:\n`{e}`")

    file_id = file.id
    # Normalize base URL: ensure scheme and no trailing slash
    base = normalize_base_url(ServerConfig.get_domain_url())

    dl_link = f"{base}/dl/{file_id}?code={secret_code}" if base else ""
    stream_link = f"{base}/stream/{file_id}?code={secret_code}" if base else ""

    # For videos or streamable files
    lang = TgConfig  # placeholder to indicate TgConfig available
    # Use configured bot language for messages
    from config import BotInfoConfig

    if (msg.document and msg.document.mime_type and 'video' in msg.document.mime_type) or msg.video:
        template = msg_translate(lang, "MediaLinksText")
        text = template % {'dl_link': dl_link, 'stream_link': stream_link}
        first_row = build_button_row([
            ('🔗 Download', dl_link if is_valid_http_url(dl_link) else ''),
            ('▶️ Stream', stream_link if is_valid_http_url(stream_link) else ''),
        ])
        buttons = [
            first_row,
            build_button_row([('❌ Revoke', f'rm_{file_id}_{secret_code}')])
        ]
    else:
        template = msg_translate(lang, "FileLinksText")
        text = template % {'dl_link': dl_link}
        buttons = [
            build_button_row([('🔗 Download', dl_link if is_valid_http_url(dl_link) else '')]),
            build_button_row([('❌ Revoke', f'rm_{file_id}_{secret_code}')])
        ]

    try:
        await msg.reply(
            text=text,
            quote=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        # Handle invalid button URL errors (eg. missing scheme in DOMAIN_URL)
        logging.exception("Failed to send message with buttons: %s", e)
        err_str = str(e)
        if 'BUTTON_URL_INVALID' in err_str or 'ButtonUrlInvalid' in err_str:
            # Send message without buttons and show cleaned links so user can still access them
            fallback_text = text + "\n\nNote: button URL was invalid — showing links inline:\n"
            fallback_text += f"Download: {dl_link}\n"
            if 'stream_link' in locals():
                fallback_text += f"Stream: {stream_link}\n"
            await msg.reply(fallback_text, quote=True)
        else:
            # Unknown error, re-raise to surface it
            raise