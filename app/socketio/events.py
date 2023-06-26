from flask_socketio import SocketIO, join_room
from flask import session
from app.socketio.answers import get_answer
from app.models.message import Message, save_message, messages_collection
from app.controllers.message_controller import get_messages
from app.models.user import find_by_id
from app.helpers.random_item import random_item
from app.data.sample_answers import sample_answers, unclear_answers


def handle_events(app):
    socketio = SocketIO(app, cors_allowed_origins="*")

    @socketio.on('send-message')
    def handle_message(data):
        message = data["message"]
        user_id = data["roomId"]
        is_logged = True
        try:
            user = find_by_id(user_id)
            if not user:
                is_logged = False
        except:
            is_logged = False
        if is_logged:
            messages = messages_collection.find({"user_id": user_id, "is_sender": False})
            for msg in messages:
                msg["id"] = str(msg["_id"])
                msg["_id"] = str(msg["_id"])
            data = get_answer(message, user_id, is_logged, messages)
            answer = data["answer"]
            if answer["content"] == "":
                answer["content"] = random_item(unclear_answers)
            socketio.emit('bot-answer', answer)
        else:
            data = get_answer(message, user_id, is_logged, session[user_id] )
            answer = data["answer"]
            if answer["content"] == "":
                answer["content"] = random_item(unclear_answers)
            session[user_id].insert(0, answer)
            socketio.emit('bot-answer', answer)
        # socketio.emit('bot-answer', "message")

    @socketio.on('connect')
    def handle_connection(data):
        print("connect::", session)

    @socketio.on('join-room')
    def handle_join_room(room_id):
        print("join_room", room_id)
        session[room_id] = []
        join_room(room_id)

    return socketio
