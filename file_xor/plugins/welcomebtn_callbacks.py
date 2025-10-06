from file_xor import roxe
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import BotInfoConfig
from file_xor.lang import msg_translate , lang

@roxe.on_callback_query(filters.regex(r"^start_back$"))
async def _help_back_cb(_, query: CallbackQuery):

    first_name = query.from_user.first_name or "there"
    caption = msg_translate(lang, "WelcomeMe").format(first_name=first_name, bot_name=BotInfoConfig.BOT_NAME)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 Updates", url="https://t.me/YourChannel"),
                InlineKeyboardButton("👨‍💻 Developer", url="https://github.com/Dot-ser"),
            ],
            [InlineKeyboardButton("Menu❤️‍🩹", callback_data="show_help")],
        ]
    )

    # Try to edit the caption (works for media messages); fall back to edit_text if needed.
    try:
        await query.message.edit_caption(caption=caption, reply_markup=buttons)
    except Exception:
        try:
            await query.message.edit_text(text=caption, reply_markup=buttons)
        except Exception:
            # If editing fails, send a new message instead
            await query.message.reply_photo(photo=BotInfoConfig.BOT_LOGO, caption=caption, reply_markup=buttons)

    await query.answer()


@roxe.on_callback_query(filters.regex(r"^show_help$"))
async def _show_help_cb(_, query: CallbackQuery):
    """Show the MenuText when user presses the inline Help button."""
    caption = msg_translate(lang, "MenuText")

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 Updates", url="https://t.me/YourChannel"),
                InlineKeyboardButton("👨‍💻 Developer", url="https://github.com/Dot-ser"),
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="start_back")],
        ]
    )

    try:
        await query.message.edit_caption(caption=caption, reply_markup=buttons)
    except Exception:
        try:
            await query.message.edit_text(text=caption, reply_markup=buttons)
        except Exception:
            await query.message.reply_photo(photo=BotInfoConfig.BOT_LOGO, caption=caption, reply_markup=buttons)

    await query.answer()