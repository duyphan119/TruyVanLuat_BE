from flask import Flask
from flask_cors import CORS
from app.routes import register_routes
from app.socketio.events import handle_events
from flask_session import Session
import os
from dotenv import load_dotenv
from datetime import timedelta
from app.config.db import client
# import nltk

# Tải các tài nguyên cần thiết
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

load_dotenv()

app = Flask(__name__)

cors = CORS(app, resources={"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['LOGGER_HANDLER_POLICY'] = 'never'
app.config['SECRET_KEY'] = os.getenv("SESSION_KEY")
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = client
app.config['SESSION_MONGODB_DB'] = os.getenv("DATABASE_NAME")
app.config['SESSION_COOKIE_NAME'] = "c-user"
app.permanent_session_lifetime = timedelta(weeks=2)

Session(app)
register_routes(app)

socketio = handle_events(app)


if __name__ == '__main__':
    try:
        socketio.run(app)
    except Exception as e:
        print(f'Error: {e}')
