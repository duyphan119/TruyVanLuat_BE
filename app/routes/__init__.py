from app.routes.group_traffic_sign_routes import group_traffic_sign_bp
from app.routes.traffic_sign_routes import traffic_sign_bp
from app.routes.crawl_routes import crawl_bp
from app.routes.violation_routes import violation_bp
from app.routes.auth_routes import auth_bp
from app.routes.message_routes import message_bp
from flask import Blueprint

routes_bp = Blueprint('routes', __name__)


def register_routes(app):
    app.register_blueprint(group_traffic_sign_bp)
    app.register_blueprint(traffic_sign_bp)
    app.register_blueprint(crawl_bp)
    app.register_blueprint(violation_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(message_bp)
