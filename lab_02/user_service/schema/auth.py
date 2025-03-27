from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None

class UserCreate(User):
    password: str

class UserInDB(User):
    hashed_password: str