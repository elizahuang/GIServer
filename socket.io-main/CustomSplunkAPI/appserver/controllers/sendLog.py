# Doc: https://wiki.splunk.com/Community:40GUIDevelopment

# Result API:
# http://localhost:8000/custom/CustomSplunkAPI/sendLog/sendLogMail?A=B

import socketio
import paramiko

sio = socketio.Client()

counter=0

@sio.event
def connect():
    print('Connected. sid:', sio.get_sid())
    
sio.connect('http://localhost:8466')
# sio.connect('http://127.0.0.1:5000/')

def _sendLogMail(**kwargs):
    sio.emit('sendLogMail', kwargs)
    # print('sendLogMail. sid:', sio.get_sid())

    global counter
    counter+=1
    print('counter:', counter)


import time
if __name__ == "__main__":
    while True:
        userinput=input('Send Something:')
        testdata={'hostname': 'host1', 'timestamp': time.time(), 'userinput': userinput}
        # print(testdata)
        _sendLogMail(**testdata)
else:
    # Attach API to Splunk
    import cherrypy
    import splunk.appserver.mrsparkle.controllers as controllers
    from splunk.appserver.mrsparkle.lib.decorators import expose_page
    from splunk.appserver.mrsparkle.lib.routes import route
    class TestController(controllers.BaseController):

        # http://localhost:8000/custom/CustomSplunkAPI/sendLog/sendLogMail?A=B
        @expose_page(must_login=True)
        def sendLogMail(self, **kwargs):
            _sendLogMail(kwargs)

        # @expose_page(must_login=True)
        # def header_echo(self, **kwargs):
        #     cherrypy.response.headers['Content-Type'] = 'text/plain'
        #     output = []
        #     for k,v in cherrypy.request.headers.items():
        #         output.append('%s: %s' % (k, v))
        #     return '\n'.join(output)


        # @route('/:path=routed')
        # @expose_page(must_login=True)
        # def request_echo(self, **kwargs):
        #     """
        #     Example handler that uses the @route() decorator to
        #     control the URI endpoint mapping
        #     """
        #     cherrypy.response.headers['Content-Type'] = 'text/plain'
        #     output = []
        #     for k,v in kwargs.items():
        #         output.append('%s: %s' % (k, v))
        #     return '\n'.join(output)
        

        # @expose_page(must_login=True)
        # def mako_template(self, **kwargs):

        #     # note the path syntax here: in order to reference templates
        #     # included in an app, use the modified path of the form:
        #     #     /<YOUR_APP_NAME>:/templates/<YOUR_TEMPLATE_NAME>
        #     return self.render_template('/network:/templates/controller_test.html', {'qs': kwargs})