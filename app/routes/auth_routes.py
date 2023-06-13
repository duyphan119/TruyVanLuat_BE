from flask import Blueprint, jsonify, request, session
from app.controllers.auth_controller import login, register, get_profile

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/register', methods=["POST"])
def route_register():
    data = register(request.json)
    session["user_id"] = data["data"]["id"]
    session["is_admin"] = data["data"]["is_admin"]
    return jsonify(data["data"]), data["status"]


@auth_bp.route('/auth/login', methods=["POST"])
def route_login():
    data = login(request.json)
    session["user_id"] = data["data"]["id"]
    session["is_admin"] = data["data"]["is_admin"]
    return jsonify(data["data"]), data["status"]


@auth_bp.route('/auth/profile', methods=["GET"])
def route_get_profile():
    print("profile::", session)

    if "user_id" in session:
        user_id = session["user_id"]
        if user_id:
            data = get_profile(user_id)
            return jsonify(data["data"]), data["status"]
    return jsonify({"message": "Chưa đăng nhập"}), 401


@auth_bp.route('/auth/logout', methods=["POST"])
def route_logout():
    session.clear()
    return jsonify({"message": "Đăng xuất thành công"}), 200
