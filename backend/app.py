from flask import Flask
from flask_socketio import SocketIO
from routes.chat import chat_bp
from routes.tasks import tasks_bp
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# Initialize SocketIO
socketio = SocketIO(app)

# Enable CORS to allow cross-origin requests (useful when React is running on a different port)
CORS(app)

# Register Blueprints
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(tasks_bp, url_prefix='/tasks')

if __name__ == "__main__":
    # Run the app with SocketIO
    socketio.run(app, debug=True)