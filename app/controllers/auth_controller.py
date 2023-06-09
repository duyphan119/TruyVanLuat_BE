from app.models.user import User, find_user, save_user, find_by_id
from werkzeug.security import generate_password_hash, check_password_hash


def register(json_data):
    email = json_data["email"]
    password = json_data["password"]
    existing_user = find_user(email)
    if existing_user:
        return {"data": {"message": "Email đã tồn tại"}, "status": 400}
    hashed_password = generate_password_hash(password)
    new_user = User(id="", email=email, password=hashed_password, full_name=json_data["full_name"],
                    phone=json_data["phone"], is_admin=False)
    _id = save_user(new_user)
    dict_user = new_user.__dict__
    dict_user.pop("password")
    dict_user["id"] = _id
    return {"data": dict_user, "status": 201}


def login(json_data):
    email = json_data["email"]
    password = json_data["password"]
    existing_user = find_user(email)
    if existing_user and check_password_hash(existing_user.password, password):
        dict_user = existing_user.__dict__
        dict_user.pop("password")
        return {"data": dict_user, "status": 201}
    return {"data": {"message": "Email hoặc mật khẩu không chính xác"}, "status": 400}


def get_profile(id):
    existing_user = find_by_id(id)
    if existing_user:
        dict_user = existing_user.__dict__
        dict_user.pop("password")
        return {"data": dict_user, "status": 201}
    return {"data": None, "status": 400}
