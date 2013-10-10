from Queue import Queue
import threading, socket, os, sys, time
from Proxy import Proxy
from ThreadPool import ThreadPoolMixIn

if __name__ == '__main__':
    from SocketServer import TCPServer
    
    class ThreadedServer(ThreadPoolMixIn, TCPServer):
        pass

    def test(HandlerClass = Proxy,
            ServerClass = ThreadedServer, 
            protocol="HTTP/1.0"):
        '''
        Test: Run an HTTP server on port 8002
        '''

        port = 8002
        server_address = ('', port)

        HandlerClass.protocol_version = protocol
        RQServer = ServerClass(server_address, HandlerClass)
        Proxy.threadServer = RQServer
        
        sa = RQServer.socket.getsockname()
        print "Serving HTTP on", sa[0], "port", sa[1], "..."
        RQServer.serve_forever()
        
        try:
            RQHandler.serve_forever()
        except KeyboardInterrupt:
            print time.asctime(), "Catched Ctrl+C, trying to shutdown", "..."
            RQHandler.server_close()
        
    test()               