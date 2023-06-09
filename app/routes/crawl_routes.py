from flask import Blueprint, jsonify
from app.controllers.crawl_controller import crawl_text

crawl_bp = Blueprint('crawl', __name__)


@crawl_bp.route('/crawl/text', methods=["GET"])
def route_crawl_text():
    data = crawl_text()
    return jsonify(data), 200
