from flask import Flask, request, render_template
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket
import json

app = Flask(__name__)

user_dict = {}


@app.route('/chat/api/<user>')
def chat_api(user):
    user_socket = request.environ.get("wsgi.websocket")
    if user_socket:
        user_dict[user] = user_socket
    while True:
        msg = json.loads(user_socket.receive())
        send_msg = {
            'msg': msg.get('msg'),
            'from_user': user,
        }
        to_user_socket = user_dict.get(msg.get('to_user'))
        to_user_socket.send(json.dumps(send_msg))


@app.route('/chat/')
def chat():
    return render_template('chat.html')


if __name__ == '__main__':
    http_serve = WSGIServer(
        ("0.0.0.0", 9527),
        app,
        handler_class=WebSocketHandler
    )
    http_serve.serve_forever()
