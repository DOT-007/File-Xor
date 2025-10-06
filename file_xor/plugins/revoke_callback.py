from pyrogram.types import CallbackQuery
from pyrogram import filters
from file_xor import roxe
from file_xor.lang import msg_translate
from file_xor.lib._StreamServer import get_message
from config import BotInfoConfig
import re
import logging


lang = BotInfoConfig.LANG


@roxe.on_callback_query(filters.regex(r"^(rm|del|revoke)_"))
async def manage_callback(bot, q: CallbackQuery):
    query = q.data or ""

    if query.startswith('rm_'):
        sq = query.split('_')

        if len(sq) != 3:
            return await q.answer(msg_translate(lang, "InvalidQueryText"), show_alert=True)

        # message id is in sq[1]
        try:
            msg_id = int(sq[1])
        except (TypeError, ValueError):
            return await q.answer(msg_translate(lang, "InvalidQueryText"), show_alert=True)

        message = await get_message(msg_id)

        if not message:
            return await q.answer(msg_translate(lang, "MessageNotExist"), show_alert=True)

        # The caption is stored like: ||sender_id=123,
        # secret_code=abcd|| (see getlink_files.py). Extract both values robustly.
        caption = message.caption or ""
        m = re.search(r"sender_id\s*=\s*(\d+).*?secret_code\s*=\s*([0-9a-fA-F]+)", caption, re.S)
        if not m:
            # If caption format is unexpected, don't allow revoke
            return await q.answer(msg_translate(lang, "MessageNotExist"), show_alert=True)

        stored_sender_id = int(m.group(1))
        stored_secret = m.group(2)

        # validate user and secret
        if q.from_user.id != stored_sender_id or sq[2] != stored_secret:
            return await q.answer(msg_translate(lang, "InvalidQueryText"), show_alert=True)

        # delete the stored message from the file DB channel
        try:
            await message.delete()
        except Exception:
            logging.exception("Failed to delete stored file message %s", msg_id)
            # Inform the user that deletion failed (permission or other error)
            return await q.answer(msg_translate(lang, "FileDeleteForbiddenText"), show_alert=True)

        await q.answer(msg_translate(lang, "LinkRevokedText"), show_alert=True)
    else:
        await q.answer(msg_translate(lang, "InvalidQueryText"), show_alert=True)