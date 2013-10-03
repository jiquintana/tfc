#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, base64, binascii
from pprint import pprint


class Proxy(BaseHTTPRequestHandler):
    
    __version__ = '0.1'
    server_version = "HTTP_Proxy/" + __version__
    realm = 'Basic realm="'+server_version+' Authentication required"'
    user = 'none'
    password= ''
    Allowed = 0
    
    def log_request(self, code='-', size='-'):
    
        """Log an accepted request.
           This is called by send_response().
   
        """
    
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
        return

    def do_HEAD_AUTH(self):
        self.send_response(407,"Proxy Authentication Required. "+self.server_version+": Access to the Web Proxy filter is denied.")
        self.send_header('Proxy-Authenticate', 'Negotiate')
        self.send_header('Proxy-Authenticate', self.realm)
        self.send_header('Via', self.server_version)
        self.send_header('Proxy-Connection', 'close')
        self.send_header('Connection', 'close')
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
        self.parsed_path = urlparse.urlparse(self.path)
	
	#pprint(parsed_path)
	'''
        #print self.log_request.code


        #      'method: '+self.headers.get('path')

        #pprint(vars(), stream=None, indent=1, width=80, depth=None)
        pprint(parsed_path)
        #pprint((vars(self)),indent=8,depth=2)
        #pprint(object, stream=None, indent=1, width=80, depth=None)
	'''

        return
    
    
    
    #TODO: Proxy-Authorization: Basic dXNlcjpwYXNzd29yZA==
    #TODO: dividir en 407 (proxy) y Authentication http
    
    def handle_PROXY_AUTH(self):
	if self.headers.has_key('Proxy-Authorization'):
	    #if self.headers.('Proxy-Authorization'):
	    #print "Got Auth"
	    self.authorization = self.headers.get('Proxy-Authorization')
	    self.authorization = self.authorization.split()
	
	    if self.authorization[0].lower() == "basic":
		try:
		    self.authorization = base64.decodestring(self.authorization[1])
		except binascii.Error:
		    pass
		else:
		    self.authorization = self.authorization.split(':')
		    self.user=self.authorization[0]
		    self.password=self.authorization[1]
		    ##print self.authorization
	
			#if self.authorization[0].upper == 'BASIC':
			#    self.userpass = base64.decodestring(self.authorization[1])
			#    print self.authorization[0]
			#    print self.authorization[1]
			    #print base64.decodestring(self.authorization[1])
			    #print self.userpass
			#print ">>> Got Auth"+base64.b64decode(self.headers.get('Proxy-Authorization'))
		    #print vars(self.headers)
		    ##pprint (vars(self))
		    ### dump headers
		    ####pprint (vars(self.headers),indent=1, width=80, depth=None)
		    
	    #self.do_HEAD()  
	    return 1
	else:
	    #print "NOT Got Auth. ASK"
	    return 0
	    #self.do_GETAUTH()
		    #self.close_connection()
	
	return
    
    def do_GET(self):
        #self.parse()
        #print(self.dump())
        self.parse_query()

	## Handle authentication

	
	
	
	if self.parsed_path.netloc =='':
	    
            self.do_HEAD()
            self.wfile.write("<HTML><BODY><PRE>"+self.dump()+"</PRE></BODY></HTML>")
	    
	    print '_ src: '+self.client_address[0] +',\tPermit:'+str(self.Allowed)+',\tUSR: '+self.user+',\tSRV: '+self.path
	    #pprint(self.parsed_path)
	    
	    
	else:
	    #print 'LOG: src: '+self.client_address[0] +', PRX: '+self.path
	    self.Allowed = self.handle_PROXY_AUTH()
	    
	    if self.Allowed == 1:
		self.do_HEAD()
	    else:
		self.do_HEAD_AUTH()	    
		
	    print '_ src: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+', USR:\t'+self.user+',\tPRX: '+self.path
	    #pprint(self.parsed_path)	    
	    
        '''
	if self.client_address[0] == '127.0.0.1':
            #self.do_HEAD()
            #self.parse_query()
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
	'''
        return

    def do_PUSH(self):
        ###self.parse()
        self.do_HEAD()
        self.wfile.write("<HTML><BODY><CODE>"+self.dump()+"</CODE></BODY></HTML>")
        return

