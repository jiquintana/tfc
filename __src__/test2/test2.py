#!/usr/bin/python
from SocketServer import ThreadingMixIn
from Queue import Queue
import threading, socket
import time
from pprint import pprint
import base64, binascii

#socket.setdefaulttimeout(3)


class ThreadPoolMixIn(ThreadingMixIn):
    '''
    use a thread pool instead of a new thread on every request
    '''
    numThreads = 1
    allow_reuse_address = True  # seems to fix socket.error on server restart

    def serve_forever(self):
        '''
        Handle one request at a time until doomsday.
        '''
        # set up the threadpool
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target=self.process_request_thread)
            t.setDaemon(1)
            t.start()

        # server main loop
        while True:
            self.handle_request()

        self.server_close()

    def process_request_thread(self):
        '''
        obtain request from queue instead of directly from server socket
        '''
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())

    def handle_request(self):
        '''
        simply collect requests and put them on the queue for the workers.
        '''
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            self.requests.put((request, client_address))

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse

class Proxy(BaseHTTPRequestHandler):
    
    __version__ = '0.1'
    server_version = "HTTP_Proxy/" + __version__
    realm = 'Basic realm="'+server_version+' Authentication required"'
    
    def log_request(self, code='-', size='-'):
    
	"""Log an accepted request.
   	   This is called by send_response().
   
	"""
      
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
        return

    def do_GETAUTH(self):
	self.send_response(407,"Proxy Authentication Required. "+self.server_version+": Access to the Web Proxy filter is denied.")
	self.send_header('Proxy-Authenticate', 'Negotiate')
	self.send_header('Proxy-Authenticate', self.realm)
	self.send_header('Via', 'Myself')
	#self.send_header('Proxy-Connection', 'close')
	#self.send_header('Connection', 'close')
	self.end_headers()
	return
    
    def dump(self):
        parsed_path = urlparse.urlparse(self.path)
        message = '\n'.join([
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                ])
	
        return message
    
    def parse_query(self):
	      #', method: '  +self.headers.get('command')
	      #', path: '    +str(self.headers.get('path'))
	parsed_path = urlparse.urlparse(self.path)
	print ' * src: ' + self.client_address[0] +\
	      ', method: ' + self.command +\
	      ', scheme: ' + parsed_path.geturl() +\
	      ', '
	pprint (parsed_path.scheme)

	
	#print self.log_request.code
	
	      
	#      'method: '+self.headers.get('path')
	
	#pprint(vars(), stream=None, indent=1, width=80, depth=None)
	pprint(parsed_path)
	#pprint((vars(self)),indent=8,depth=2)
	#pprint(object, stream=None, indent=1, width=80, depth=None)
	
	
	return
        
    def do_GET(self):
	#self.parse()
	print ('client_address=%s (%s)' % (self.client_address, self.address_string()))
	print '>> request from:: '+self.client_address[0]+':'+str(self.client_address[1])
	#print(self.dump())
	if self.client_address[0] == '127.0.0.1':
	    self.do_HEAD()	    
	    self.parse_query()
	    #self.wfile.write("<HTML><BODY><PRE>"+self.dump()+"</PRE></BODY></HTML>")
	    
	    
	    #self.send_response(200)
	    ##self.end_headers()	
	    #self.wfile.write("<HTML><BODY></BODY></HTML>")	    
	else:
	    print '>>> foreign'
	    if self.headers.has_key('Proxy-Authorization'):
		#if self.headers.('Proxy-Authorization'):
		self.authorization = self.headers.get('Proxy-Authorization')
		self.authorization = self.authorization.split()
		
		if self.authorization[0].lower() == "basic":
		    try:
			self.authorization = base64.decodestring(self.authorization[1])
		    except binascii.Error:
			pass
		    else:
			self.authorization = self.authorization.split(':')
			print self.authorization
			
		#if self.authorization[0].upper == 'BASIC':
		#    self.userpass = base64.decodestring(self.authorization[1])
		#    print self.authorization[0]
		#    print self.authorization[1]
		    #print base64.decodestring(self.authorization[1])
		    #print self.userpass
		#print ">>> Got Auth"+base64.b64decode(self.headers.get('Proxy-Authorization'))
	    ##print vars(self.headers)
	    ##pprint (vars(self))
	    #pprint (vars(self.headers))
	    
	    
	    self.do_GETAUTH()
	    #self.close_connection()
	    
        return        

    def do_PUSH(self):
        ###self.parse()
        self.do_HEAD()  
        self.wfile.write("<HTML><BODY><CODE>"+self.dump()+"</CODE></BODY></HTML>")
        return        
      
        

if __name__ == '__main__':
    from SocketServer import TCPServer

    class ThreadedServer(ThreadPoolMixIn, TCPServer):
        pass

    #def test(HandlerClass=SimpleHTTPRequestHandler,
    def test(HandlerClass=Proxy,
            ServerClass=ThreadedServer,
            protocol="HTTP/1.0",
            server_version="blah"):
        '''
        Test: Run an HTTP server on port 8002
        '''

        port = 8003
        server_address = ('', port)

        HandlerClass.protocol_version = protocol
        httpd = ServerClass(server_address, HandlerClass)

        sa = httpd.socket.getsockname()
        #print "Serving HTTP on", sa[0], "port", sa[1], "..."
	print time.asctime(), "ServerHTTP started on", sa[0], "port", sa[1], "..."
        httpd.serve_forever()

    try:
	test()
    except KeyboardInterrupt:
	pass


	print time.asctime(), "Server stop"
