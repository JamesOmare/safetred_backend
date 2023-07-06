from fastapi import APIRouter, HTTPException, status
from schemas.user import UserAuth, UserCreate, UserGet
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from service.user import UserService
from model.users import Users
from ...user_deps import get_current_user
from db_setup import get_db


user_router = APIRouter()

@user_router.post('/create', summary="Create new user", response_model=UserAuth)
async def create_user(data: UserAuth, db: Session = Depends(get_db)):
    try:
        return await UserService.create(db, data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )



@user_router.get('/me', summary='Get details of currently logged in user', response_model=UserGet)
async def get_me(user: Users = Depends(get_current_user)):
    return user


@user_router.post('/update', summary='Update User', response_model=UserCreate)
async def update_user(data: UserCreate, user: Users = Depends(get_current_user)):
    try:
        return await UserService.update_user(user.id, data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )