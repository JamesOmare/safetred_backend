
from sqlalchemy.future import select
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import update as sql_update
from model.users import Users
from schemas.user import UserAuth, UserCreate
from db_setup import commit_roll_back
from security import get_password_hash, verify_password
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = Users(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password),
            phone_number=user.phone_number,
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
        await user_in.save()
        return user_in

    @staticmethod
    async def authenticate(db: Session, email: str, password: str) -> Optional[Users]:
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.password):
            return None
        
        return user
    
    # @staticmethod
    # async def authenticate(db: Session, username: str, password: str) -> Optional[Users]:
    #     user = await UserService.get_user_by_username(db, username)
    #     if not user:
    #         return None
    #     if not verify_password(password=password, hashed_pass=user.password):
    #         return None
        
    #     return user
   
    # Non-async version of authenticate method above 
    # @staticmethod
    # def authenticate(db: Session, username: str, password: str) -> Optional[Users]:
    #     user = UserService.get_user_by_username(db, username)
    #     if not user:
    #         return None
    #     if not verify_password(password=password, hashed_pass=user.password):
    #         return None
        
    #     return user
    
    @staticmethod
    async def get_by_email(db: Session, email: str) -> Optional[Users]:
        # This will take the first 'User' with the email 'email
        query = db.query(Users).filter(Users.email == email).first()
        await db.execute(query)
        return query
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Users:
        query = select(Users).where(Users.email == email)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Users:
        query = select(Users).where(Users.username == username)
        result = await db.execute(query)
        user = result.scalars().first()
        return user

    
    @staticmethod
    async def update_password(db: Session, email: str, password: str):
        query = sql_update(Users).where(Users.email == email).values(
            password=password).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_roll_back()
        
    
    @staticmethod
    async def update_user(db: Session, id: int, data: UserCreate) -> Users:
        # user = await Users.find_one(Users.id == id)
        user = db.query(Users).filter(Users.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
            
         # Update user fields based on the provided data
        user.email = data.email
        user.username = data.username
        user.password = data.password
        user.phone_number = data.phone_number
        user.is_active = data.is_active
        user.is_superuser = data.is_superuser

        await db.commit()
        await db.refresh(user)
        return user
    
    # @staticmethod
    # async def get_user_by_id(id: UUID) -> Optional[Users]:
    #     user = await Users.find_one(Users.id == id)
    #     return user

    
    async def create(db: Session, user: Users):
            db_user = Users(
                email=user.email,
                username=user.username,
                password= get_password_hash(user.password),
                phone_number=user.phone_number,
                is_active=user.is_active,
                is_superuser=user.is_superuser
                )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
    
    async def get_user_by_id(db: AsyncSession, id: int) -> Users:
        query = select(Users).where(Users.id == id)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    # non-async version of get_by_username query
    # def get_user_by_username(db: Session, username: str) -> Users:
    #     user = db.query(Users).filter(Users.username == username).first()
    #     return user


    # async def get_user_by_email(db: Session, email) -> Users:
    #     return await db.query(Users).filter(Users.email == email).first()
    
    

    
    
    
    


    # @staticmethod
    # async def get_user_profile(username:str):
    #     query = select(Users.username, 
    #                     Users.email, 
    #                     Person.name, 
    #                     Person.birth,
    #                     Person.sex,
    #                     Person.profile,
    #                     Person.phone_number).join_from(Users,Person).where(Users.username == username)
    #     return(await db.execute(query)).mappings().one()
