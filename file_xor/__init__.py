# Version: 1.0 Beta
# ©️ 2021 DOTSERMODZ ALL RIGHTS RESERVED
import logging
import sys
from pyrogram import Client
from config import TgConfig
from logging import getLogger
from logging.config import dictConfig
from config import LOGGER_CONFIG_JSON


# Configure configured handlers (file handlers, etc.) first
dictConfig(LOGGER_CONFIG_JSON)
# Replace/augment stream handler with colored console output

version = 1.0
logger = getLogger('file_xor')



_BANNER = """ 
\033[36m___________________________________________________________
\033[36m-----------------------------------------------------------
\033[36m-----------------------------------------------------------

\033[34m██████╗░░█████╗░███████╗███████╗░██████╗░░░░░░██╗░░██╗
\033[34m██╔══██╗██╔══██╗╚════██║██╔════╝██╔════╝░░░░░░╚██╗██╔╝
\033[34m██████╔╝██║░░██║░░███╔═╝█████╗░░╚█████╗░█████╗░╚███╔╝░
\033[34m██╔══██╗██║░░██║██╔══╝░░██╔══╝░░░╚═══██╗╚════╝░██╔██╗░
\033[34m██║░░██║╚█████╔╝███████╗███████╗██████╔╝░░░░░░██╔╝╚██╗
\033[34m╚═╝░░╚═╝░╚════╝░╚══════╝╚══════╝╚═════╝░░░░░░░╚═╝░░╚═╝
\033[36m-----------------------------------------------------------
\033[33m🇩​​​​​🇴​​​​​🇹​​​​​🇸​​​​​🇪​​​​​🇷​​​​​🇲​​​​​🇴​​​​​🇩​​​​​🇿 🇧​​​​​🇴​​​​​🇹​​​​​ - 🇸​​​​​🇹​​​​​🇦​​​​​🇷​​​​​🇹​​​​​🇮​​​​​🇳​​​​​🇬​​​​​...
\033[35mDeveloper : \033[32m[DOT-007](https://alosious-benny.vercel.app)
\033[35mVersion   : \033[37m1.0 Beta
\033[35mPython    : \033[37m3.9.6
\033[35mLibrary   : \033[37mPyrogram & Pyrofork
\033[31m©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
\033[36m-----------------------------------------------------------
\033[36m-----------------------------------------------------------
\033[36m___________________________________________________________
\033[0m

""" 





logger = logging.getLogger(__name__)
logger.info(_BANNER)
logger.info("Starting dotsermodz-basebot (v1.0 Beta)")

# Ensure pyrogram logs don't flood; but we want bot logs shown at INFO
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("bot").setLevel(logging.INFO)

roxe = Client(
    "dotsermodz-basebot",
    bot_token=TgConfig.BOT_TOKEN,
    api_id=TgConfig.API_ID,
    api_hash=TgConfig.API_HASH,
    plugins=dict(root="file_xor/plugins"),
    sleep_threshold=-1,
    max_concurrent_transmissions=10,
)
