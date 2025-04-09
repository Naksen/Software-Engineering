import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError

from core.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")
SECRET_KEY = "46c12329dbcfb211caf39f5c58a65b1cb9f30407fc2d72f4b9d416ebd301cecb"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return TokenData(username=username)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
