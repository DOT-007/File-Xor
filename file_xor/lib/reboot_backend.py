import os
import sys
import asyncio
import logging

logging.basicConfig(level=logging.INFO)


async def graceful_shutdown(bot):
    """Stop the bot cleanly.

    `bot` is expected to have a `.stop()` coroutine (Pyrogram client).
    """
    await bot.stop()


def restart_process():
    """Restart the current Python process in place.

    Note: this will not return.
    """
    os.execl(sys.executable, sys.executable, *sys.argv)
