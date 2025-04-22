from .database import folders_collection, emails_collection

def init_db():
    folders_collection.delete_many({})
    emails_collection.delete_many({})

    folders_collection.create_index("name", unique=True)

    folder = {"name": "Main Folder", "username": "admin"}
    folders_collection.insert_one(folder)

    email = {
        "subject": "First message",
        "content": "Hello!",
        "sender": "admin",
        "recipients": ["user"],
        "folder_name": "Main Folder",
        "username": "admin"
    }
    emails_collection.insert_one(email)
