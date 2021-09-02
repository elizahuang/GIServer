#!/usr/bin/python

# A Socket.io client in Admin for retrieving log

import socketio
import paramiko
import asyncio
import time

counter=0

async def Client(url):
    namespace = '/admin'
    # sio = socketio.Client()
    sio = socketio.AsyncClient()

    @sio.event(namespace=namespace)
    def connect():
        print(f"{url} {sio.get_sid(namespace=namespace)} connected")

    # @sio.event
    # def connect_error(data):
    #     print("The connection failed")

    @sio.event(namespace=namespace)
    def disconnect():
        print(f"{url} {sio.get_sid(namespace=namespace)} disconnected")

    @sio.event(namespace=namespace)
    def getLog(request):
        # print(url, sio.get_sid(namespace=namespace), '>', getLog.__name__, ':', request)
        print('>', getLog.__name__)

        time.sleep(3)
        # asyncio.sleep(3)
        # # Use SSH Lib 'paramiko'
        # ip = "192.168.1.20"
        # username = "itmanager"
        # password = "P@ssw0rd"

        # client = paramiko.SSHClient()
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.connect(ip, port=22, username=username, password=password, timeout=20)
        # # client.exec_command('echo P@ssw0rd | sudo -S reboot')
        # # client.exec_command('echo Hello from Admin zone > splunk_admin_client.txt')
        # stdin, stdout, stderr = client.exec_command('ls -l')
        # stdout = stdout.read()
            
        # client.close()

        # Use 'subprocess'
        from subprocess import check_output
        stdout=check_output(['date', '-R']).decode()
        
        logResult={'stdout': stdout, 'request': request}
        await sio.emit('logResult', logResult, namespace=namespace)
        # print(url, sio.get_sid(namespace=namespace), '< logResult:', logResult)
        print('< logResult:', logResult)

        global counter
        counter+=1
        print('counter:', counter)


    try:
        await sio.connect(url, namespaces=[namespace])
        await sio.wait()
    except Exception as e:
        print(f"Can't connect to {url}:", e)
        return

urls=['http://localhost:8466']
tasks = [Client(url) for url in urls]
asyncio.run(asyncio.wait(tasks))