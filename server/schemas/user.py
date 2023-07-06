from pydantic import BaseModel, validator
from fastapi import HTTPException
import logging
import re
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
# get root logger
logger = logging.getLogger(__name__)

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email", unique=True)
    username: str = Field(..., min_length=5, max_length=50, description="user username", unique=True)
    password: str = Field(..., min_length=5, description="user password")
    phone_number: str = Field(..., min_length=10, max_length=30, description="user phone number", unique=True)
    is_active: bool = True
    is_superuser: bool = False
    
    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator: {v}")

        # regex phone number
        regex = r"^[\+]?[(]?[0-9]{4}[)]?[-\s\.]?[0-9]{4}[-\s\.]?[0-9]{4,6}$"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail="Invalid input phone number!")
        return v

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "username": "example",
                "password": "weakpassword",
                "phone_number": "2547890223412",
                "is_active": True,
                "is_superuser": False
            }
        }
        
class UserGet(BaseModel):
    email: EmailStr
    username: str
    phone_number: str
    is_active: bool = True
    is_superuser: bool = False
    
    class Config:
        orm_mode = True
 

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    phone_number: str
    is_active: bool = True
    is_superuser: bool = False
    
    # phone number validation

    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator: {v}")

        # regex phone number
        regex = r"^[\+]?[(]?[0-9]{4}[)]?[-\s\.]?[0-9]{4}[-\s\.]?[0-9]{4,6}$"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail="Invalid input phone number!")
        return v
    
    class Config:
        orm_mode = True

class User(UserCreate):
    id: int

    class Config:
        orm_mode = True
