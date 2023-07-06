from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import get_settings
from typing import Generator

# DATABASE_URL="postgresql://postgres:foxtrot09er@localhost:5432/safetred"

engine = create_async_engine(
    get_settings().db_url, future=True, echo=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)

# not_async_engine = create_engine(
#     DATABASE_URL, echo=True
# )
# Not_Async_SessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=not_async_engine
# )

# def not_async_get_db():
#     db = Not_Async_SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

Base = declarative_base()

  
# Dependency      
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.commit()
            await db.close()

        
async def commit_roll_back():
    db = SessionLocal()
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
