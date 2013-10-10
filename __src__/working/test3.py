#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import threading, socket, os, sys, time
from Queue import Queue
from Proxy import Proxy
from ThreadPool import ThreadPoolMixIn
from SocketServer import TCPServer

class ThreadedServer(ThreadPoolMixIn, TCPServer):
    pass

def run(HandlerClass = Proxy,
        ServerClass = ThreadedServer, 
        protocol="HTTP/1.0"):
    '''
    Run an HTTP server on port 8002
    '''
    port = 8002
    server_address = ('', port)

    HandlerClass.protocol_version = protocol
    RQServer = ServerClass(server_address, HandlerClass)
    Proxy.threadServer = RQServer
    
    sa = RQServer.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    try:
        RQServer.serve_forever()
    except KeyboardInterrupt:
        print time.asctime(), "Catched Ctrl+C, trying to shutdown", "..."
        RQServer.server_close()
        os._exit(1)
    
    #RQHandler.serve_forever()


if __name__ == '__main__':       
    run()               
