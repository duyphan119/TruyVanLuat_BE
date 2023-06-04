from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes import register_routes
from app.socketio.events import handle_events

load_dotenv()

app = Flask(__name__)

register_routes(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['LOGGER_HANDLER_POLICY'] = 'never'


socketio = handle_events(app)


if __name__ == '__main__':
    socketio.run(app)
