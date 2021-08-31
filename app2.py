# https://python-socketio.readthedocs.io/en/latest/server.html
from flask import Flask
from flask_cors import CORS
import socketio

sio = socketio.Server(async_mode='threading',cors_allowed_origins='*')
app = Flask(__name__)
CORS(app)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
client_sid=None

# ... Socket.IO and Flask handler functions ...
@app.route("/testLogRequest")
async def testLogRequest():
    await sio.emit('getLog', to=client_sid)
    return ('finish emit')

@sio.on('logResult')
def logResult(sid, log_result):
    print('log_result:\n',log_result)

@sio.event
def connect(sid, environ, auth):
    client_sid=sid
    print('connect ', client_sid)

@sio.event
def disconnect(sid):
    print('disconnect ', client_sid)




if __name__ == '__main__':
    app.run()
