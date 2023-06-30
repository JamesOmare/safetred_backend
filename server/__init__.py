# from fastapi import FastAPI
# import logging
# from logging.config import dictConfig
# from config import LogConfig
# from server.database import db

# dictConfig(LogConfig().dict())
# logger = logging.getLogger("mycoolapp")

# def create_app():
#     db.init()
    
#     app = FastAPI(
#         title="SafeTred API",
#         description="API for SafeTred",
#         version="0.1.0",
#     )
    
#     @app.on_event("startup")
#     async def startup():
#         await db.create_all()
        
#     @app.on_event("shutdown")
#     async def shutdown():
#         await db.close()
        
#     return app