from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token, authenticate_user, get_password_hash, get_user as get_db_user
from models.user import User as DBUser
from schema.auth import Token, UserInDB, User, UserCreate
from api.deps import get_current_active_user, get_db
from datetime import timedelta

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[Session, Depends(get_db)],
) -> Token:
    user = authenticate_user(db_session, form_data.username, form_data.password)
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
async def create_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_db)],
    user: UserCreate,
):
    existing_user = get_db_user(db_session, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user.password)

    new_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        disabled=False,
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

@router.get("/users/{username}", response_model=User)
async def get_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_db)],
    username: str
):
    existing_user = get_db_user(db_session, username)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return existing_user

@router.delete("/users/{username}")
async def delete_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_db)],
    username: str
):
    user = get_db_user(db_session, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_session.delete(user)
    db_session.commit()

    return {"message": "User deleted successfully"}