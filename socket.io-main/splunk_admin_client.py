#!/usr/bin/python

# A Socket.io client in Admin for retrieving log

import socketio
import paramiko
import threading
import time
from queue import Queue

counter = 0
namespace = '/admin'
queue = Queue()

def Client(url, queue):
    sio = socketio.Client()

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
        global counter
        counter+=1
        print('> getLog', counter)
        # print(id(queue._loop))
        # asyncio.run(queue.put([request, sio, counter]))
        queue.put([request, sio, counter])

    try:
        sio.connect(url, namespaces=[namespace])
        sio.wait()
    except Exception as e:
        print(f"Can't connect to {url}:", e)
        return


def main():
    # print(id(asyncio.get_event_loop()))
    urls = ['http://localhost:8466']
    threads = []
    for url in urls:
        thread=threading.Thread(target = Client, args = (url, queue))
        thread.start()
        threads.append(thread)

    while True:
        request, sio, count = queue.get()
        time.sleep(1)
        
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
        stdout = check_output(['date', '-R']).decode()

        # emit result
        logResult = {'stdout': stdout, 'request': request}
        sio.emit('logResult', logResult, namespace=namespace)
        # print(url, sio.get_sid(namespace=namespace), '< logResult:', logResult)
        print('< logResult', count)

    for thread in threads:
        thread.join()

main()