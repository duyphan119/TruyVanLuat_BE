from flask import Blueprint, jsonify,request
from app.controllers.traffic_sign_controller import get_traffic_signs, create_traffic_sign

traffic_sign_bp = Blueprint('traffic_sign', __name__)


@traffic_sign_bp.route('/traffic-signs', methods=["GET"])
def route_get_traffic_signs():
    limit = request.args.get('limit') or '-1'
    page = request.args.get('p') or '-1'
    sort_by = request.args.get('sort_by') or 'code'
    sort_type = request.args.get('sort_type') or 'DESC'
    limit = int(limit)
    page = int(page)
    data = get_traffic_signs(page, limit, sort_by, sort_type)
    return jsonify(data), 200

@traffic_sign_bp.route('/traffic-signs', methods=["POST"])
def route_create_traffic_sign():
    data = create_traffic_sign(request.json)
    return jsonify(data), 201