from app.config.db import db
from bson.objectid import ObjectId
from datetime import datetime

users_collection = db['users']

class User:
    def __init__(self, id, email, password, full_name, phone, is_admin):
        self.id = id
        self.email = email
        self.password = password
        self.full_name = full_name
        self.phone = phone
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

def save_user(user):
    user_data = {
        'full_name': user.full_name,
        'email': user.email,
        'password': user.password,
        'phone': user.phone,
        'is_admin': user.is_admin,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
    }
    saved = users_collection.insert_one(user_data)
    return str(saved.inserted_id)

def find_user(email):
    user_data = users_collection.find_one({'email': email})
    if user_data:
        return User(id=str(user_data["_id"]), email=user_data["email"], password=user_data["password"], full_name=user_data["full_name"], phone=user_data["phone"], is_admin=user_data["is_admin"])
    return None

def find_by_id(id):
    user_data = users_collection.find_one({'_id': ObjectId(id)})
    if user_data:
        print(user_data)
        return User(id=str(user_data["_id"]), email=user_data["email"], password=user_data["password"], full_name=user_data["full_name"], phone=user_data["phone"], is_admin=user_data["is_admin"])
    print("No data")
    return None
