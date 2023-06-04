from flask import Blueprint, jsonify
from app.controllers.traffic_sign_controller import get_traffic_signs

traffic_sign_bp = Blueprint('traffic_sign', __name__)


@traffic_sign_bp.route('/traffic-sign')
def route_get_traffic_signs():
    data = get_traffic_signs()
    return jsonify(data), 200
