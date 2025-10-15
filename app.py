import eventlet
eventlet.monkey_patch()  # MUST be first

from flask import Flask, render_template
from flask_socketio import SocketIO, send
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'  # change this later
socketio = SocketIO(app, cors_allowed_origins="*")

CHAT_FILE = 'chat_history.json'

def load_messages():
    try:
        with open(CHAT_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_message(msg):
    messages = load_messages()
    messages.append(msg)
    with open(CHAT_FILE, 'w') as f:
        json.dump(messages, f)

messages = load_messages()

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    messages.append(msg)
    save_message(msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)



