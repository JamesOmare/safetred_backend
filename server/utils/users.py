from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from model.users import Users
from schemas.user import UserCreate


async def get_user(db: AsyncSession, user_id: int):
    query = select(Users).where(Users.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Users).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = Users(email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user