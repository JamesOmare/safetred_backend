import uvicorn
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from typing_extensions import Annotated
from typing import List
import config
import logging
from logging.config import dictConfig
from config import LogConfig
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from fastapi.responses import JSONResponse
from api.api_v1.router import router
from datetime import datetime
import json

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

origins= [
    "http://localhost:3001"
]

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

app.add_middleware(DBSessionMiddleware, db_url=get_settings().db_url)

app.add_middleware(
                 
                    CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"] 
                   
                )

app.include_router(router, prefix=get_settings().API_V1_STR)

class ConnectionManager:

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/server_info")
async def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    logger.error("logging from the root logger")
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
    }

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            message = {"time":current_time,"clientId":client_id,"message":data}
            await manager.broadcast(json.dumps(message))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time":current_time,"clientId":client_id,"message":"Offline"}
        await manager.broadcast(json.dumps(message))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    
# uvicorn main:app --reload