from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes import register_routes
from app.socketio.events import handle_events
from flask_session import Session
import os
from datetime import timedelta

load_dotenv()

app = Flask(__name__)


cors = CORS(app, resources={"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['LOGGER_HANDLER_POLICY'] = 'never'
app.config['SECRET_KEY'] = os.getenv("SESSION_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
app.permanent_session_lifetime = timedelta(weeks=2)

Session(app)
register_routes(app)

socketio = handle_events(app)


if __name__ == '__main__':
    socketio.run(app)
