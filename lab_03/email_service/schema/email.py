from pydantic import BaseModel
from typing import List

class EmailFolderCreate(BaseModel):
    name: str

class EmailFolder(BaseModel):
    id: int
    name: str

class EmailCreate(BaseModel):
    subject: str
    content: str
    sender: str
    recipients: List[str]

class Email(BaseModel):
    id: int
    subject: str
    content: str
    sender: str
    recipients: List[str]
    folder_id: int
