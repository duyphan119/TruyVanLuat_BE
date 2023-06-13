from flask_socketio import SocketIO, join_room
from flask import session
from app.socketio.answers import get_answer
from app.models.message import Message, save_message


def handle_events(app):
    socketio = SocketIO(app, cors_allowed_origins="*")

    @socketio.on('send-message')
    def handle_message(data):
        # print('received message:', data)
        # answer = get_answer(data)
        # message = Message(id="",content=answer, intent="", entities=[], user_id="")
        # _id = save_message(message)
        # dict_message = message.__dict__
        # dict_message["id"] = _id
        message = data["message"]
        user_id = data["roomId"]
        answer = get_answer(message)
        socketio.emit('bot-answer', answer)
        # socketio.emit('bot-answer', "message")

    @socketio.on('connect')
    def handle_connection(data):
        print("connect::", session)

    @socketio.on('join-room')
    def handle_join_room(room_id):
        print("join_room", room_id)
        join_room(room_id)

    return socketio
