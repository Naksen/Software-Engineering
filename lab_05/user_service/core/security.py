from datetime import datetime, timedelta, timezone
import json

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from sqlalchemy.orm import Session

from models.user import User
from schema.auth import TokenData
from core.config import SECRET_KEY, ALGORITHM
from core.redis import redis_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(db_session: Session, username: str, password: str):
    user = get_user(db_session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def serialize_user(user: User):
    return json.dumps({
        "username": user.username,
        "email": user.email,
        "disabled": user.disabled,
        "hashed_password": user.hashed_password,
    })

def deserialize_user(data: str):
    obj = json.loads(data)
    return User(**obj)

def get_user_with_cache(db_session: Session, username: str):
    cached = redis_client.get(f"user:{username}")
    if cached:
        return deserialize_user(cached)

    user = db_session.query(User).filter(User.username == username).first()
    if user:
        redis_client.set(f"user:{username}", serialize_user(user))
    return user

def get_user(db_session: Session, username: str):
    return db_session.query(User).filter(User.username == username).first()
        
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return TokenData(username=username)
    except jwt.PyJWTError:
        return None
