from app.config.db import db
from bson.objectid import ObjectId
from datetime import datetime

messages_collection = db['messages']

class Message:
    def __init__(self, id, user_id, content, intent, entities, is_sender):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.intent = intent
        self.entities = entities
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_sender = is_sender

def save_message(message):
    message_data = {
        'user_id': message.user_id,
        'content': message.content,
        'intent': message.intent,
        'entities': message.entities,
        'created_at': message.created_at,
        'updated_at': message.updated_at,
        'is_sender': message.is_sender
    }
    saved = messages_collection.insert_one(message_data)
    return str(saved.inserted_id)

def save_message_json(message_data):
    saved = messages_collection.insert_one(message_data)
    return str(saved.inserted_id)

def find_by_user_id(user_id):
    messages = messages_collection.find({"user_id": user_id})
    return messages
