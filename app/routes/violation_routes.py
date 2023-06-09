from flask import Blueprint, jsonify, request
from app.controllers.violation_controller import search_violations, get_violation_by_id

violation_bp = Blueprint('violation', __name__)


@violation_bp.route('/violations/search', methods=["GET"])
def route_search_violations():
    keyword = request.args.get('keyword') or ''
    limit = request.args.get('limit') or '10'
    page = request.args.get('p') or '1'
    limit = int(limit)
    page = int(page)
    data = search_violations(keyword, limit, page)
    return jsonify(data), 200


@violation_bp.route('/violations/<id>', methods=["GET"])
def route_get_violation_by_id(id):
    data = get_violation_by_id(id)
    return jsonify(data), 200
