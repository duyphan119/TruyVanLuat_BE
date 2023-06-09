from pymongo import MongoClient
import os 

client = MongoClient(os.getenv("DATABASE_URL"))

db = client[os.getenv("DATABASE_NAME")]
