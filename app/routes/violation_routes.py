from flask import Blueprint, jsonify, request
from app.controllers.violation_controller import search_violations, get_violation_by_id, update_violation, get_related_violations, get_classes

violation_bp = Blueprint('violation', __name__)


@violation_bp.route('/violations/search', methods=["GET"])
def route_search_violations():
    keyword = request.args.get('keyword') or ''
    sort_by = request.args.get('sort_by') or 'mavipham'
    sort_type = request.args.get('sort_type') or 'ASC'
    limit = request.args.get('limit') or '10'
    page = request.args.get('p') or '1'
    limit = int(limit)
    page = int(page)
    data = search_violations(keyword, limit, page, sort_by, sort_type)
    return jsonify(data), 200


@violation_bp.route('/violations/classes', methods=["GET"])
def route_get_classes():
    data = get_classes()
    return jsonify(data), 200


@violation_bp.route('/violations/<id>', methods=["GET"])
def route_get_violation_by_id(id):
    data = get_violation_by_id(id)
    return jsonify(data), 200


@violation_bp.route('/violations/related/<id>', methods=["GET"])
def route_get_related_violation_by_id(id):
    data = get_related_violations(id)
    return jsonify(data), 200


@violation_bp.route('/violations/<id>', methods=["PATCH"])
def route_update_violation(id):
    data = update_violation(id, request.json)
    return jsonify(data), 200
