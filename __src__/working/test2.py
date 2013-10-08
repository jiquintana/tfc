#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number


import socket, time, signal, os
from pprint import pprint
from ThreadPool import ThreadPoolMixIn
from Proxy import Proxy
from SocketServer import TCPServer


#if os.name import Console




if __name__ == '__main__':   
 
    if os.name == 'nt':
        import Console
        win32Cons= Console.Console()
        win32Cons.process_Ctrl_C()
    
    class ThreadedServer(ThreadPoolMixIn, TCPServer):        
        KEEP_RUNNING = True
        ## Changed: Start
        daemon_threads = True
        ## Changed: End
        numThreads=5
        
        
        def keep_running(self):
            return ThreadedServer.KEEP_RUNNING        
        
        def force_shutdown(self):
            ThreadedServer.KEEP_RUNNING=False
    
           
        
    def run(HandlerClass=Proxy,
             ServerClass=ThreadedServer,
             protocol="HTTP/1.0",
             server_version="MyProxyServer"):    
        port = 8002
        server_address = ('', port)
        HandlerClass.protocol_version = protocol
        Atiende = ServerClass(server_address, HandlerClass)
        Proxy.threadServer = Atiende
        print "Jose es un tocapelota: ", Proxy.threadServer

        sa = Atiende.socket.getsockname()
        print time.asctime(), "ServerHTTP started on", sa[0], "port", sa[1], "..."
        
        
        
        
        '''try:
            Atiende.serve_forever()
        except KeyboardInterrupt:
            print time.asctime(), "Catched Ctrl+C, trying to shutdown", "..."
            
            Atiende.server_close()
            print time.asctime(), "ServerHTTP Shutdown", "..."
            pass
        '''
        
        while Atiende.keep_running():
            print "Jose es un tocapelotas"
            #Atiende.handle_request()
            #Atiende.serve_forever()
                 
        
                
   
    run() 