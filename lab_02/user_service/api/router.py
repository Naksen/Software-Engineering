from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from core.config import fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token, authenticate_user, get_password_hash
from schema.auth import Token, UserInDB, User, UserCreate
from api.deps import get_current_active_user
from datetime import timedelta

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        disabled=user.disabled,
    )

    fake_users_db[user.username] = new_user
    return new_user

@router.get("/users/{username}", response_model=User)
async def get_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str
):
    if username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_users_db[username]

@router.delete("/users/{username}")
async def delete_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str
):
    if username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del fake_users_db[username]
    return {"message": "User deleted successfully"}