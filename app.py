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
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.message import EmailMessage
# from subprocess import check_output
import subprocess
import aiosmtplib
import logging
import shutil

sio = socketio.AsyncServer(async_mode='aiohttp',cors_allowed_origins='*')
APP = web.Application()
sio.attach(APP)
client_sid=None
admin_client_sid=None


async def testLogRequest(req: Request):
    await sio.emit('getLog', to=client_sid)
    print('finish emit')


async def sendMailX(req=None,dataToSend=None):
    #hostname, timestamp, 機器類型, 廠商的mail, serial_number(index=bare_metal)
    testData={'hostname':'testinghostAAA',
              'timestamp':1630466370,
              'machine_type':'DELL',
              'manufacture':'DELL',
              'destin_mail_address':'ihuang@tsmc.com',
              'serial_num':'SE123456', 
              'logs':{'log_name1':'teststring11111teststring11111teststring11111teststring11111',
                      'log_name2':'teststring222teststring222teststring222',
                      'log_name3':'teststring33333teststring33333teststring33333'}}
    
    dataToSend=testData
    logs=dataToSend.pop('logs')
    destin_mail_address=dataToSend.pop('destin_mail_address')
    dirPath= os.path.join(os.path.dirname(__file__), str(dataToSend['timestamp']))
    os.mkdir(dirPath)
    for key,value in logs.items():          
        completeName = os.path.join(dirPath, str(key)+".txt")
        f = open(completeName, "x")
        f.write(str(value))
        f.close()
        # f = open(completeName, "r")
        # print(f.read())
    
    completeName = os.path.join(dirPath, "needRepairInfo.txt")
    f = open(completeName, "x")
    f.write(str(dataToSend))
    f.close()
    # f = open(completeName, "r")
    # print(f.read())

    mailxCommand=['mailx','-s','tsmc'+testData['machine_type']+'repair']
    for path in os.listdir(dirPath):
        full_path = os.path.join(dirPath, path)
        if os.path.isfile(full_path):
            mailxCommand.append('-a')
            mailxCommand.append(str(full_path))
    mailxCommand.append(str(destin_mail_address))
    print('mailxCommand:',mailxCommand)
    # print(subprocess.check_output(mailxCommand).decode())
    shutil.rmtree(dirPath)



# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the event we wish to listen out for
@sio.on('logResult')
async def logResult(sid, log_result):
    print('log_result:\n',log_result)


@sio.on('sendLogMail')
async def sendLogMail(sid, dataToSend):
    print('dataToSend:\n',dataToSend)
    await sendMailX(dataToSend)
    await sio.emit('getLog',dataToSend, to=admin_client_sid, namespace='/admin')

@sio.on('connect')
def connect(sid, environ, auth):
    global admin_client_sid,client_sid
    client_sid=sid
    print('connect client_sid:', client_sid,end="\n\n")

@sio.on('connect', namespace='/admin')
def admin_connect(sid, environ, auth):
    global admin_client_sid,client_sid
    admin_client_sid=sid
    print('connect admin_client_sid:', admin_client_sid,end="\n\n")

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect client_sid:',client_sid,end="\n\n")

@sio.on('disconnect', namespace='/admin')
def admin_disconnect(sid):
    print('disconnect admin_client_sid:',admin_client_sid,end="\n\n")


APP.router.add_get('/testLogRequest', testLogRequest)
APP.router.add_get('/testMailX',sendMailX)

if __name__ == "__main__":
    try:
        import sys
        port = int(sys.argv[1])
        # port = os.getenv('PORT', default=8080)
        web.run_app(APP,port=port)

    except Exception as error:
        raise error
