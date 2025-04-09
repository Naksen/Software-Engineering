from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class EmailFolder(Base):
    __tablename__ = "email_folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, index=True)

    emails = relationship("Email", back_populates="folder")


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    content = Column(String)
    sender = Column(String)
    recipients = Column(String)
    folder_id = Column(Integer, ForeignKey("email_folders.id"))

    folder = relationship("EmailFolder", back_populates="emails")