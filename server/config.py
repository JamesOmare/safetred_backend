from dotenv import load_dotenv
from decouple import config
import logging
from functools import lru_cache
from pydantic import BaseSettings, BaseModel


load_dotenv()

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    # we can use SECRET_KEY:str or DATABASE_URL: str only(if it matches the name in .env file)
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES:  int
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM : str
    API_V1_STR: str
    db_url: str = config("DATABASE_URL")
    app_name: str = "SafeTred API"
    environment: str = "dev"
    testing: bool = False
    debug: bool = True
    
    
    class Config:
        env_prefix = ''
        env_file = '.env' 

    

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "mycoolapp"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


@lru_cache()
def get_settings() -> BaseSettings:
    settings = Settings()
    log.info("Loading config settings from the environment...")
    return settings