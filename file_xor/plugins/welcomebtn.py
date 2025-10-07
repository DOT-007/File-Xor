from file_xor import roxe
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import BotInfoConfig
from file_xor.lang import msg_translate , lang
from file_xor.lib.isVerify import isPrivate , isBanned


@roxe.on_message(filters.command(["start", "help"]))
@isPrivate 
@isBanned
async def start_command(_, message: Message):
    first_name = message.from_user.first_name or "there"
    cmd = message.command[0]

    caption = (
        msg_translate(lang, "WelcomeMe").format(first_name=first_name, bot_name=BotInfoConfig.BOT_NAME)
        if cmd == "start"
        else msg_translate(lang, "MenuText")
    )

    # Base URL buttons shown in both start and help
    base_buttons = [
        [
            InlineKeyboardButton("Script 👨🏻‍💻", url="https://github.com/Dot-ser/File-Xor"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://github.com/Dot-ser"),
        ]
    ]

    # On the welcome view, show a Help button; on the help view, show a Back button
    if cmd == "start":
        base_buttons.append([InlineKeyboardButton("Menu❤️‍🩹", callback_data="show_help")])
    elif cmd == "help":
        base_buttons.append([InlineKeyboardButton("🔙 Back", callback_data="start_back")])

    buttons = InlineKeyboardMarkup(base_buttons)

    await message.reply_photo(
        photo=BotInfoConfig.BOT_LOGO,
        caption=caption,
        reply_markup=buttons,
    )



