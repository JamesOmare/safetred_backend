from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from service.user import UserService
from security import create_access_token, create_refresh_token
from schemas.auth_schema import TokenSchema
from schemas.user import UserCreate
from model.users import Users
from ..user_deps import get_current_user
from config import get_settings
from schemas.auth_schema import TokenPayload
from pydantic import ValidationError
from sqlalchemy.orm import Session
from jose import jwt
from db_setup import get_db, not_async_get_db


auth_router = APIRouter()


@auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = await UserService.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }

# Non async version of function above
# @auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(not_async_get_db)) -> Any:
#     user = UserService.authenticate(db, username=form_data.username, password=form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect username or password"
#         )
    
#     return {
#         "access_token": create_access_token(user.id),
#         "refresh_token": create_refresh_token(user.id),
#     }


@auth_router.post('/test-token', summary="Test if the access token is valid", response_model=UserCreate)
async def test_token(user: Users = Depends(get_current_user)):
    return user


@auth_router.post('/refresh', summary="Refresh token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, get_settings().JWT_REFRESH_SECRET_KEY, algorithms=[get_settings().ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }