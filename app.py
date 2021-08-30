# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys,os,json
import socketio
from datetime import datetime

from aiohttp import web
from aiohttp.web import Request, Response, json_response

sio = socketio.AsyncServer(async_mode='aiohttp',cors_allowed_origins='*')
APP = web.Application()#middlewares=[aiohttp_error_middleware]
sio.attach(APP)
client_sid=None


async def testLogRequest(req: Request):
    await sio.emit('getLog', to=client_sid)
    print('finish emit')


# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the event we wish to listen out for
@sio.on('logResult')
async def logResult(sid, log_result):
    print('log_result:\n',log_result)

@sio.event
def connect(sid, environ, auth):
    client_sid=sid
    print('connect ', client_sid)

@sio.event
def disconnect(sid):
    print('disconnect ', client_sid)

APP.router.add_get('/testLogRequest', testLogRequest)

if __name__ == "__main__":
    try:

        port = os.getenv('PORT', default=8080)
        web.run_app(APP,port=port)
    except Exception as error:
        raise error
