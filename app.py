from collections import defaultdict
from flask import Flask, request
from flask_socketio import SocketIO
from database_connections import db_init, add_message_thread, add_message

from typing import List, Dict, Set, Tuple

app = Flask("web_server")

socketio = SocketIO(app, cors_allowed_origins="*")

db = db_init()

page_sids: Dict[str, Set[str]] = defaultdict(set)
user_to_page: Dict[str, str] = {}
thread_messages: Dict[str, List[dict]] = defaultdict(list)
page_threads: Dict[str, List[str]] = defaultdict(list)
mouse_pos: Dict[str, Tuple[int, int]] = {}
sids = set()

# own webserver
@app.route("/")
def root_page():
    return "hello"


@socketio.on("connect")
def connected():
    print(f"client with sid {request.sid} connected")


@socketio.on("connect_to_doc")
def handle_host_connect(msg):
    sid = request.sid
    sids.add(sid)
    user_id = msg["user"]
    page_url = msg["url"]
    page_sids[page_url].add(sid)
    user_to_page[user_id] = page_url
    print(f"client {user_id} connected to page {page_url}")

    # Send party ID back to the host
    socketio.emit("connect_to_doc", f"connected to doc {page_url}!", room=sid)


def _add_msg_content(msg):
    def add_thread():
        user_id = msg["user"]
        page_url = user_to_page[user_id]
        page_threads[page_url].append(msg["message_thread_id"])
        add_message_thread(
            db, {"x": msg["x"], "y": msg["y"], "id": msg["message_thread_id"]}
        )

    thread_id = msg["message_thread_id"]
    if thread_id not in thread_messages:
        add_thread()

    new_msg = {"user": msg["user"], "body": msg["body"], "timestamp": msg["timestamp"]}
    thread_messages[msg["message_thread_id"]].append(new_msg)
    add_message(db, new_msg, msg["message_thread_id"])


@socketio.on("add_msg")
def add_msg(msg):
    user_id = msg["user"]
    print(f"{user_id} sent msg: {msg}")
    _add_msg_content(msg)

    # Send party ID back to the all users connected to the doc except for sending user
    for sid in sids:
        if sid != request.sid:
            socketio.emit("add_msg", msg, room=sid)


@socketio.on("move_cursor")
def move_cursor(msg):
    user_id = msg["user"]
    mouse_pos[user_id] = (msg["x"], msg["y"])

    for sid in sids:
        if sid != request.sid:
            socketio.emit("move_cursor", msg, room=sid)


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=8080)
