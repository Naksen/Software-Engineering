from fastapi import APIRouter, Depends, HTTPException
from schema.email import EmailFolder, EmailFolderCreate, Email, EmailCreate
from core.security import get_current_user
from typing import List

router = APIRouter()

user_folders_db: dict[str, List[EmailFolder]] = {
    "admin": [EmailFolder(id=1, name="Main Folder")]
}
user_emails_db: dict[str, List[Email]] = {
    "admin": [
        Email(
            id=1,
            subject="First message",
            content="Hello !",
            sender="admin",
            recipients=["user"],
            folder_id=1
        )
    ]
}

@router.post("/folders/", response_model=EmailFolder)
async def create_folder(folder: EmailFolderCreate, user=Depends(get_current_user)):
    username = user.username
    if username not in user_folders_db:
        user_folders_db[username] = []
    
    folder_id = len(user_folders_db[username]) + 1
    new_folder = EmailFolder(id=folder_id, name=folder.name)
    user_folders_db[username].append(new_folder)
    return new_folder

@router.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, user=Depends(get_current_user)):
    username = user.username
    if username not in user_folders_db:
        raise HTTPException(status_code=404, detail="User has no folders")
    
    user_folders_db[username] = [f for f in user_folders_db[username] if f.id != folder_id]
    user_emails_db[username] = [email for email in user_emails_db[username] if email.folder_id != folder_id]
    return {"message": "Folder deleted"}

@router.get("/folders/", response_model=List[EmailFolder])
async def get_folders(user=Depends(get_current_user)):
    return user_folders_db.get(user.username, [])

@router.post("/folders/{folder_id}/emails/", response_model=Email)
async def create_email(folder_id: int, email: EmailCreate, user=Depends(get_current_user)):
    username = user.username
    if username not in user_emails_db:
        user_emails_db[username] = []
    
    email_id = len(user_emails_db[username]) + 1
    new_email = Email(id=email_id, folder_id=folder_id, **email.dict())
    user_emails_db[username].append(new_email)
    return new_email

@router.get("/folders/{folder_id}/emails/", response_model=List[Email])
async def get_emails(folder_id: int, user=Depends(get_current_user)):
    username = user.username
    return [e for e in user_emails_db.get(username, []) if e.folder_id == folder_id]
