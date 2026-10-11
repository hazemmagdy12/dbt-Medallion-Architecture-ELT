import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
DB_NAME = "burger_app_db"

def get_database():
    """
    الدالة دي بتعمل الاتصال بالسيرفر وترجع الداتا بيز جاهزة للاستخدام.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        client.admin.command('ping') 

        print(f"Successfully connected to MongoDB. Database: {DB_NAME}")
        
        return client[DB_NAME]
        
    except ConnectionFailure as e:
        print(f"[-] Database connection failed: {e}")
        raise
db=get_database()