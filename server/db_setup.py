from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings



engine = create_async_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)

# async with engine.begin() as conn:
#     await conn.run_sync(Base.metadata.drop_all)
# async with engine.begin() as conn:
#     await conn.run_sync(Base.metadata.create_all)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
async def async_get_db():
    async with SessionLocal() as db:
        yield db
        await db.commit()
        
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

# async def commit_roll_back():
#     try:
#         await db.commit()
#     except Exception:
#         await db.rollback()
#         raise
