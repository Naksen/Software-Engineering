from fastapi import APIRouter, Depends, HTTPException
from schema.email import EmailFolder, EmailFolderCreate, Email, EmailCreate
from core.security import get_current_user
from core.database import folders_collection, emails_collection
from typing import List

router = APIRouter()

@router.post("/folders/", response_model=EmailFolder)
async def create_folder(
    folder: EmailFolderCreate,
    user=Depends(get_current_user),
):
    username = user.username
    doc = {"name": folder.name, "username": user.username}
    result = folders_collection.insert_one(doc)
    return {**doc, "id": result.inserted_id}

@router.delete("/folders/{folder_name}")
async def delete_folder(
    folder_name: str,
    user=Depends(get_current_user),
):
    result = folders_collection.delete_one({
        "name": folder_name,
        "username": user.username
    })

    emails_collection.delete_many({
        "folder_name": folder_name,
        "username": user.username
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Folder not found")

    return {"message": "Folder deleted"}

@router.get("/folders/", response_model=List[EmailFolder])
async def get_folders(user=Depends(get_current_user)):
    return folders_collection.find({"username": user.username}).to_list(length=100)

@router.post("/folders/{folder_name}/emails/", response_model=Email)
async def create_email(
    folder_name: str,
    email: EmailCreate,
    user=Depends(get_current_user),
):
    folder = folders_collection.find_one({
        "name": folder_name,
        "username": user.username
    })
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    doc = {
        "subject": email.subject,
        "content": email.content,
        "sender": email.sender,
        "recipients": email.recipients,
        "folder_name": folder_name,
        "username": user.username
    }

    result = emails_collection.insert_one(doc)
    return {**doc, "id": str(result.inserted_id)}

@router.get("/folders/{folder_name}/emails/", response_model=List[Email])
async def get_emails(folder_name: str, user=Depends(get_current_user)):
    emails = emails_collection.find({
        "folder_name": folder_name,
        "username": user.username
    }).to_list(length=100)

    for email in emails:
        email["id"] = str(email["_id"])
    return emails
