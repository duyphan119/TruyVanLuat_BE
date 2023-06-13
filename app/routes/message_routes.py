from flask import Blueprint, jsonify, request, session, abort
from app.controllers.message_controller import save_message, get_messages
from app.middlewares.is_logged import is_logged

message_bp = Blueprint('message', __name__)

@message_bp.before_request
def before_request():
    # Kiểm tra route hiện tại
    current_route = request.endpoint

    # Áp dụng middleware cho từng route cụ thể
    if current_route == 'route_create_message':
        pass
    elif current_route == 'route_create_message':
        logged = is_logged(session)
        if logged:
            pass
        else:
            abort(401)

@message_bp.route('/messages', methods=["GET"])
def route_get_messages():
    if "user_id" in session:
        data = get_messages(session["user_id"])
        return jsonify(data["data"]), data["status"]
    return jsonify([]), 200


@message_bp.route('/messages', methods=["POST"])
def route_create_message():
    data = save_message(request.json, session["user_id"])
    return jsonify(data["data"]), data["status"]
