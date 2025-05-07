from pydantic import BaseModel
from typing import List

class EmailFolderCreate(BaseModel):
    name: str

class EmailFolder(BaseModel):
    _id: str
    name: str
    username: str

class EmailCreate(BaseModel):
    subject: str
    content: str
    sender: str
    recipients: List[str]

class Email(BaseModel):
    _id: str
    subject: str
    content: str
    sender: str
    recipients: List[str]
    username: str
