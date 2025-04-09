import os
from datetime import timedelta

from schema.auth import UserInDB

SECRET_KEY = "46c12329dbcfb211caf39f5c58a65b1cb9f30407fc2d72f4b9d416ebd301cecb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TOKEN_EXPIRE_TIME = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
DATABASE_URL = "postgresql://postgres:postgres@database:5432/main_db"

