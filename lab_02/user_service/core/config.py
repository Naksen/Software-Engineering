from datetime import timedelta

from schema.auth import UserInDB

SECRET_KEY = "46c12329dbcfb211caf39f5c58a65b1cb9f30407fc2d72f4b9d416ebd301cecb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TOKEN_EXPIRE_TIME = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

fake_users_db = {
    "admin": UserInDB(
        username="admin",
        email="admin@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        disabled=False,
        full_name="Admin",
    ),
    "user": UserInDB(
        username="user",
        email="user@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        disabled=False,
        full_name="User",
    )
}
