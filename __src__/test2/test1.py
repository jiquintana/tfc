#!/bin/python
#from SocketServer import ThreadingMixIn
import SocketServer
import Queue
import threading, socket

class _ThreadPoolMixIn(SocketServer.ThreadingMixIn):
	'''
	Uses a thread from a thread pool instead of instantiate a new one on every request.
	'''
	numThreads = None

	def __init__(self, numThreads):
		'''
		Sets up the threadPool and "fills" it with the threads.xi
		'''
		self.numThreads = numThreads
		self.requests = Queue.Queue(self.numThreads)
		for n in range(self.numThreads):
			t = threading.Thread(target = self.process_request_thread)
			t.setDaemon(1)
			t.start()

	
	def process_request(self, request, client_address):
		'''
		Simply collect requests and put them on the queue for the workers.
		'''
		self.requests.put((request, client_address))

	def process_request_thread(self):
		'''
		Obtains request and client_address from the queue instead of directly from a call
		'''

		# The thread starts and stays on this loop.
		# The method call hangs waiting until something is inserted into self.requests
		#  and .get() unblocks
		while True:
			SocketServer.ThreadingMixIn.process_request_thread(self, *self.requests.get())
			# http://docs.python.org/tut/node6.html#SECTION006740000000000000000


class ThreadingPoolTCPServer(_ThreadPoolMixIn, SocketServer.TCPServer):
	"""
	Calls the __init__ from both super.
	"""

	def __init__(self, server_address, RequestHandlerClass, numThreads,\
		bind_and_activate=True):

		_ThreadPoolMixIn.__init__(self, numThreads)
		SocketServer.TCPServer.allow_reuse_address = True
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

class ThreadingPoolUDPServer(_ThreadPoolMixIn, SocketServer.UDPServer):
	"""
	Calls the __init__ from both super.
	"""

	def __init__(self, server_address, RequestHandlerClass, numThreads,\
		bind_and_activate=True):

		_ThreadPoolMixIn.__init__(self, numThreads)
		SocketServer.UDPServer.allow_reuse_address = True
		SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == '__main__':
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	from SocketServer import TCPServer
   

	#class ThreadingPoolTCPServer(_ThreadPoolMixIn, SocketServer.TCPServer):
	#class ThreadedServer(ThreadPoolMixIn, TCPServer):
		#pass

	def test(HandlerClass = SimpleHTTPRequestHandler,
		#ServerClass = ThreadedServer, 
		#protocol="HTTP/1.0"):
		ServerClass = ThreadingPoolTCPServer, 
		protocol="HTTP/1.0"):
		'''
		def __init__(self, server_address, RequestHandlerClass, numThreads,\
 		bind_and_activate=True):

		Test: Run an HTTP server on port 8002
		'''
		threads=1000
		port = 8002
		server_address = ('', port)

		HandlerClass.protocol_version = protocol
		httpd = ServerClass(server_address, HandlerClass, threads)

		sa = httpd.socket.getsockname()
		print "Serving HTTP on", sa[0], "port", sa[1], "..."
		httpd.serve_forever()

	test()
