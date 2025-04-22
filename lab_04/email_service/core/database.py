from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

client = MongoClient(MONGO_URL)
db = client.email_db

folders_collection = db.email_folders
emails_collection = db.emails
