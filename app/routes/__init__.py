from app.routes.traffic_sign_routes import traffic_sign_bp
from flask import Blueprint

routes_bp = Blueprint('routes', __name__)


def register_routes(app):
    app.register_blueprint(traffic_sign_bp)
