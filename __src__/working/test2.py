#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

#from SocketServer import ThreadingMixIn
#from Queue import Queue
#import threading, socket
import socket, time, signal
from pprint import pprint
from ThreadPool import ThreadPoolMixIn
from Proxy import Proxy
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer

class ThreadedServer(ThreadPoolMixIn, TCPServer):
    numThreads=5
    pass
        


def test(HandlerClass=Proxy,
         ServerClass=ThreadedServer,
         protocol="HTTP/1.0",
         server_version="blah"):
    '''
    Test: Run an HTTP server on port 8002
    '''

    port = 8002
    server_address = ('', port)

    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    #print "Serving HTTP on", sa[0], "port", sa[1], "..."
    print time.asctime(), "ServerHTTP started on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()
    
    def done():
        ThreadedServer.shutdown(self)
        

def Exit_gracefully(signal, frame):
    test.done()
    print time.asctime(), "Server stop"
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, Exit_gracefully)
    test()
        