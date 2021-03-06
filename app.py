
from gevent import monkey
monkey.patch_all()

import html


import redis
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)


@app.route('/')
def main():
    c = db.incr('connected')
    return render_template('main.html')


@app.route('/pymeetups/')
def pymeetups():
    return render_template('pymeetups.html')


@socketio.on('connect', namespace='/dd')
def ws_conn():
    c = db.incr('connected')
    socketio.emit('msg', {'count': c}, namespace='/dd')


@socketio.on('disconnect', namespace='/dd')
def ws_disconn():
    c = db.decr('connected')
    socketio.emit('msg', {'count': c}, namespace='/dd')

@socketio.on('city', namespace='/dd')
def ws_city(message):
    print(message['city'])
    socketio.emit('city', {'city': html.escape(message['city'])},
                  namespace="/dd")

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000)