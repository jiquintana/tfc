#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number


import socket, time, signal
from pprint import pprint
from ThreadPool import ThreadPoolMixIn
from Proxy import Proxy
from SocketServer import TCPServer

if __name__ == '__main__':   
    
    class ThreadedServer(ThreadPoolMixIn, TCPServer):
        ## Changed: Start
        daemon_threads = True
        ## Changed: End
        numThreads=5
        pass
            
        
    def ProxyServer(HandlerClass=Proxy,
             ServerClass=ThreadedServer,
             protocol="HTTP/1.0",
             server_version="MyProxyServer"):    
        port = 8002
        server_address = ('', port)
        HandlerClass.protocol_version = protocol
        proxyServer = ServerClass(server_address, HandlerClass)
    
        sa = proxyServer.socket.getsockname()
        print time.asctime(), "ServerHTTP started on", sa[0], "port", sa[1], "..."

        try:
            proxyServer.serve_forever()
        except KeyboardInterrupt:
            print time.asctime(), "Catched Ctrl+C, trying to shutdown", "..."
            
            proxyServer.server_close()
            print time.asctime(), "ServerHTTP Shutdown", "..."
            #proxyServer.shutdown()
            pass
        
        return proxyServer
        
                
    ProxyServer()
        