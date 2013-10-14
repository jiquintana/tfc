#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

#https://github.com/pirateproxy/PirateProxy/blob/master/pirateproxy-0.4/Proxy.py
#http://stackoverflow.com/questions/4287019/stuck-with-python-http-server-with-basic-authentication-using-basehttp/8153189#8153189
#http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
#http://stackoverflow.com/questions/2018026/should-i-use-urllib-or-urllib2-or-requests
#http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
#http://stackoverflow.com/questions/7942547/using-or-in-sqlalchemy



from SocketServer import ThreadingMixIn
from Queue import Queue
import threading
import threading, socket, os, sys, time

import socket

class ThreadPoolMixIn(ThreadingMixIn):
    '''
    use a thread pool instead of a new thread on every request
    '''
    numThreads = 10
    allow_reuse_address = True  # seems to fix socket.error on server restart
    KEEP_RUNNING = True
    ## Changed: Start
    daemon_threads = True
    ## Changed: End

    def keep_running(self):
        return self.KEEP_RUNNING        
    
    def force_shutdown(self):
        self.KEEP_RUNNING=False
        print time.asctime(), "ServerHTTP Forced Shutdown", "..."
        os._exit(0)

      
    def serve_forever(self):
        '''
        Handle one request at a time until doomsday.
        '''
        # set up the threadpool
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target = self.process_request_thread)
            t.setDaemon(1)
            t.start()

        # server main loop
        while self.keep_running():
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


