from quart import Quart
from uvicorn import Server as UvicornServer, Config
from logging import getLogger
from config import ServerConfig, LOGGER_CONFIG_JSON
from . import WebErrorHandling as error, main

# Ensure colored console handler is installed (uses LOGGER_CONFIG_JSON)

logger = getLogger('uvicorn')
instance = Quart(__name__)
instance.config['RESPONSE_TIMEOUT'] = None
instance.config['MAX_CONTENT_LENGTH'] = 999999999999999

@instance.before_serving
async def before_serve():
    logger.info('Website Launched!')
    logger.info(f'web service on {ServerConfig.BIND_ADDRESS}:{ServerConfig.PORT} ')

instance.register_blueprint(main.bp)

instance.register_error_handler(400, error.invalid_request)
instance.register_error_handler(404, error.not_found)
instance.register_error_handler(405, error.invalid_method)
instance.register_error_handler(error.HTTPError, error.http_error)

levanter = UvicornServer (
    Config (
        app=instance,
        host=ServerConfig.BIND_ADDRESS,
        port=ServerConfig.PORT,
        log_config=LOGGER_CONFIG_JSON
    )
)