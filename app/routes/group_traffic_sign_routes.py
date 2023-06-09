from flask import Blueprint, jsonify, request
from app.controllers.group_traffic_sign_controller import get_group_traffic_signs, create_group_traffic_sign

group_traffic_sign_bp = Blueprint('group_traffic_sign', __name__)


@group_traffic_sign_bp.route('/group-traffic-signs', methods=["GET"])
def route_get_group_traffic_signs():
    limit = request.args.get('limit') or '-1'
    page = request.args.get('p') or '-1'
    sort_by = request.args.get('sort_by') or 'name'
    sort_type = request.args.get('sort_type') or 'ASC'
    limit = int(limit)
    page = int(page)
    data = get_group_traffic_signs(page, limit, sort_by, sort_type)
    return jsonify(data), 200


@group_traffic_sign_bp.route('/group-traffic-signs', methods=["POST"])
def route_create_group_traffic_sign():
    data = create_group_traffic_sign(request.json)
    return jsonify(data), 201
