import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, send
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

CHAT_FILE = "chat_history.json"


# --- Load and save messages ---
def load_messages():
    try:
        with open(CHAT_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_messages(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)


# --- Initialize message list ---
messages = load_messages()


@app.route("/")
def index():
    return render_template("index.html")


# --- SocketIO Events ---
@socketio.on("connect")
def handle_connect():
    # Send all stored messages to the user who just connected
    for msg in messages:
        send(msg)


@socketio.on("message")
def handle_message(msg):
    print(f"Message received: {msg}")
    messages.append(msg)
    save_messages(messages)  # persist to file
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
