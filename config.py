from dotenv import load_dotenv
import os
from file_xor.lib.runtime_utils import load_host_url

# Load dotenv and override any existing environment variables so
# values in config.env (like LANG) take precedence over the system env.
load_dotenv("config.env", override=True)


class TgConfig:
    # Telegram related configurations
    API_ID = int(os.environ.get("API_ID", "123456"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    FILEDB_CHANNEL = int(os.environ.get("FILEDB_CHANNEL", "-1001234567890"))
   

class ServerConfig:
    # Server related configurations
    DOMAIN_URL = os.environ.get("DOMAIN_URL", "")
    DOWNLOAD_PATH = os.environ.get("DOWNLOAD_PATH", "./downloads")
    MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", "2048"))  # in MB
    GEN_SECRET_KEY_LENGTH = int(os.environ.get("GEN_SECRET_KEY_LENGTH", "8"))
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "1"))  # in MB
    BIND_ADDRESS = os.environ.get("BIND_ADDRESS", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "8000"))

    @classmethod
    def get_domain_url(cls) -> str:
        """Return configured DOMAIN_URL or fallback to runtime HOST_URL.

        Ensures no trailing slash and has scheme via URL utils where used.
        """
        if cls.DOMAIN_URL and str(cls.DOMAIN_URL).strip():
            return cls.DOMAIN_URL.strip()
        # Fallback from runtime.py if available
        host = load_host_url()
        return host or ""

class BotInfoConfig:
    # Bot related configurations    
    BOT_NAME = os.environ.get("BOT_NAME", "file_xor")
    BOT_LOGO = os.environ.get("BOT_LOGO", "https://files.catbox.moe/x7bhxz.jpg")
    OWNER_ID = int(os.environ.get("OWNER_ID", "123456789"))
    SUDO = list(map(int, os.environ.get("SUDO", "0").split(',')))
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    MODE = os.environ.get("MODE", "private").lower() 
    LANG = os.environ.get("LANG", "en")  # Default language code


LOGGER_CONFIG_JSON = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'serverlogging.log',
            'formatter': 'default'
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'uvicorn.error': {
            'level': 'WARNING',
            'handlers': ['file_handler', 'stream_handler']
        },
        'bot': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'pyrogram': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        }
    }
}