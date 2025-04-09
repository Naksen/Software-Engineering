from fastapi import APIRouter, Depends, HTTPException
from schema.email import EmailFolder, EmailFolderCreate, Email, EmailCreate
from core.security import get_current_user, get_db
from models.email import Email as DBEmail, EmailFolder as DBEmailFolder
from typing import List

router = APIRouter()

@router.post("/folders/", response_model=EmailFolder)
async def create_folder(
    folder: EmailFolderCreate,
    user=Depends(get_current_user),
    db_session=Depends(get_db),
):
    username = user.username
    db_folder = DBEmailFolder(
        name=folder.name,
        username=username,
    )
    db_session.add(db_folder)
    db_session.commit()
    db_session.refresh(db_folder)
    return db_folder

@router.delete("/folders/{folder_id}")
async def delete_folder(
    folder_id: int,
    user=Depends(get_current_user),
    db_session=Depends(get_db),
):
    username = user.username
    folder = db_session.query(DBEmailFolder).filter_by(id=folder_id, username=username).first()
    if not folder:
        raise HTTPException(status_code=400, detail="Folder was not found")

    db_session.query(DBEmail).filter(DBEmail.folder_id == folder_id).delete()
    db_session.delete(folder)
    db_session.commit()

    return {"message": "Folder deleted"}

@router.get("/folders/", response_model=List[EmailFolder])
async def get_folders(user=Depends(get_current_user), db_session=Depends(get_db)):
    return db_session.query(DBEmailFolder).filter(DBEmailFolder.username == user.username).all()

@router.post("/folders/{folder_id}/emails/", response_model=Email)
async def create_email(
    folder_id: int,
    email: EmailCreate,
    user=Depends(get_current_user),
    db_session=Depends(get_db)
):
    db_email = DBEmail(
        subject=email.subject,
        content=email.content,
        sender=email.sender,
        recipients=",".join(email.recipients),
        folder_id=folder_id,
    )
    db_session.add(db_email)
    db_session.commit()
    db_session.refresh(db_email)
    return Email(
        id=db_email.id,
        subject=db_email.subject,
        content=db_email.content,
        sender=db_email.sender,
        recipients=db_email.recipients.split(","),
        folder_id=db_email.folder_id,
    )
@router.get("/folders/{folder_id}/emails/", response_model=List[Email])
async def get_emails(folder_id: int, user=Depends(get_current_user), db_session=Depends(get_db)):
    emails = db_session.query(DBEmail).filter_by(folder_id=folder_id).all()
    for e in emails:
        e.recipients = e.recipients.split(",")
    return emails
