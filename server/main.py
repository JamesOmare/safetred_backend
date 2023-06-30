import uvicorn
from fastapi import FastAPI, Depends
from typing_extensions import Annotated
import config
import logging
from logging.config import dictConfig
from config import LogConfig
from fastapi_sqlalchemy import DBSessionMiddleware, db
from config import get_settings

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

# logger.info("Dummy Info")
# logger.error("Dummy Error")
# logger.debug("Dummy Debug")
# logger.warning("Dummy Warning")
# # setup loggers
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# # get root logger
# logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 

    
app = FastAPI(
    title="SafeTred API",
    description="API for SafeTred",
    version="0.1.0",
)

app.add_middleware(DBSessionMiddleware, db_url = get_settings().db_url)


@app.get("/server_info")
async def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    logger.error("logging from the root logger")
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    
# uvicorn main:app --reload