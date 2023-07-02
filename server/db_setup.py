from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import get_settings
from typing import Generator

DATABASE_URL="postgresql://postgres:foxtrot09er@localhost:5432/safetred"

engine = create_async_engine(
    get_settings().db_url, future=True, echo=True
)

not_async_engine = create_engine(
    DATABASE_URL, echo=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)

Not_Async_SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=not_async_engine
)

Base = declarative_base()

# Dependency
def not_async_get_db():
    db = Not_Async_SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.commit()
            await db.close()

        
        
# async def async_get_db():
#     async with SessionLocal() as db:
#         yield db
#         await db.commit()
        
# async def init_db():
#     try:
#         Base.metadata.create_all(bind=engine)
#     except Exception as e:
#         raise e

# class AsyncDatabaseSession:
#     def __init__(self):
#         self.session = None
#         self.engine = None
        
#     def __getattr__(self, name):
#         return getattr(self.session, name)
    
#     def init(self):
#         self.engine = create_async_engine(get_settings().db_url, echo=True, future=True)
#         self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        

#     async def create_all(self):
#         async with self.engine.begin() as conn:
#             await conn.run_sync(SQLModel.metadata.create_all)


# db = AsyncDatabaseSession()

async def commit_roll_back():
    db = SessionLocal()
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
