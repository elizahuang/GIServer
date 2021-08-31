# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys,os,json
import socketio
from datetime import datetime
from aiohttp import web
from multidict import MultiDict
from aiohttp.web import Request, Response, json_response
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.message import EmailMessage
import aiosmtplib
import logging

sio = socketio.AsyncServer(async_mode='aiohttp',cors_allowed_origins='*')
APP = web.Application()
sio.attach(APP)
client_sid=None


async def testLogRequest(req: Request):
    await sio.emit('getLog', to=client_sid)
    print('finish emit')

async def testSendEmail(req: Request):
    import smtplib
    sender = 'yiiiiihuang@gmail.com'
    receivers = ['ihuang@tsmc.com','chtuz@tsmc.com','henry88819@gmail.com']# ['ihuang@tsmc.com']
    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')   # 发送者
    message['To'] =  Header("测试", 'utf-8')        # 接收者
    
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com',port=587)#'localhost'
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login('yiiiiihuang@gmail.com', 'Taigidian2021')
        smtpObj.sendmail(sender, receivers, message.as_string()) 
        smtpObj.quit()        
        print ("Successfully sent email")
        return Response(status=200,content_type='text/plain')
    except:
        logging.exception("message")
        print ("Error: unable to send email")
        return Response(status=500,content_type='text/plain')
    # message = EmailMessage()
    # message["From"] = "root@localhost"
    # message["To"] = "ihuang@tsmc.com"
    # message["Subject"] = "Hello World!"
    # message.set_content("Sent via aiosmtplib")
    # await aiosmtplib.send(message, hostname="127.0.0.1", port=25)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(aiosmtplib.send(message, hostname="127.0.0.1", port=25))


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
APP.router.add_get('/testSendEmail',testSendEmail)

if __name__ == "__main__":
    try:

        port = os.getenv('PORT', default=8080)
        web.run_app(APP,port=port)
    except Exception as error:
        raise error
