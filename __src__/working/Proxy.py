#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import urlparse, base64, binascii, re
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from pprint import pprint



class Proxy(BaseHTTPRequestHandler):
    threadServer = None
    __version__ = '0.1'
    server_version = "HTTP_Proxy/" + __version__
    realm = 'Basic realm="'+server_version+' Authentication required"'
    user = 'none'
    password= ''
    Allowed = 0
    
    LocalServices = {
        re.compile(r"/STOP/", re.IGNORECASE),
        re.compile(r"/CONFIG/", re.IGNORECASE)
    }
    
    def __init__(self, request, client_address, server):
	BaseHTTPRequestHandler.__init__(self, request, client_address, server)
    

    def svc_hndl_STOP(self,parms):
	print "svc_hndl_STOP called with parms: "+parms	
	#Proxy.threadServer.server_close()
	#print Proxy.threadServer.force_shutdown
	print Proxy.threadServer.keep_running()
	Proxy.threadServer.force_shutdown()
	print Proxy.threadServer.keep_running()
	return
    
    def svc_hndl_CONFIG(self,parms):
	print "svc_hndl_CONFIG called with parms:"+parms
	return
    
    def svc_hndl_NOOP(self,parms):
	print "svc_hndl_UNDEF called with parms:"+parms
	return

    
    ServiceHandle = {
        "STOP": svc_hndl_STOP,
        "CONFIG": svc_hndl_CONFIG,
        "NOOP": svc_hndl_NOOP
    }
     
   	    
    def log_request(self, code='-', size='-'):
    
        """Log an accepted request.
           This is called by send_response().
   
        """
    
    def do_HEAD(self):
	self.send_response(200)
	if self.bodySize != None:
	    self.send_header('Content-Type', 'text/html;charset=UTF-8')
	    self.send_header('Content-Length', self.bodySize)	
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
        self.parsed_path = urlparse.urlparse(self.path)	
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
	
	# Tenemos una cabecera con autenticacion Proxy?
	if self.headers.has_key('Proxy-Authorization'):
	    self.authorization = self.headers.get('Proxy-Authorization')
	    self.authorization = self.authorization.split()
	
	    # Han usado una autenticación básica?
	    if self.authorization[0].lower() == "basic":
		try:
		    # Sí, intentamos obtener el usuario y passwd
		    self.authorization = base64.decodestring(self.authorization[1])
		
		except binascii.Error:
		    # Error, entonces KO
		    return 0 
		    
		else:
		    # Tenemos usuario & paswd y lo hemos podido decodificar
		    self.authorization = self.authorization.split(':')
		    self.user=self.authorization[0]
		    self.password=self.authorization[1]
		    if self.user == 'proxyUser' and self.password == 'proxyPass':
			#Autenticacion = OK
			return 1
		    else:
			#Autenticacion = KO
			return 0	    
    
	# No está autenticado
	else:
	    return 0
	
    
    def do_GET(self):
        self.parse_query()
	

	# Comprobamos si nos están pidiendo nuestra URL
	# Por defecto no nos piden a nosotros
	selfquery = False
	
	if self.parsed_path.netloc =='':
	    selfquery = True;
	elif self.parsed_path.netloc =='127.0.0.1':
	    selfquery = True;
	elif self.parsed_path.netloc =='localhost':
	    selfquery = True;
	
	# Si es una dirección local, atendemos la petición HTTP
	if selfquery:
	    
	    pprint(self.parsed_path)

	    service_handle_value="NOOP"
	    for URL in self.LocalServices:
		
		print "\tm"+URL.pattern
		if URL.match(self.parsed_path.path):
		    #print re.sub(URL.pattern.upper())
		    # Sustituimos el patron entre "/" y hacemos strip de los caracteres adicionales
		    
		    service_handle_value=re.sub(r"/[.]*$","",re.sub(r"^/+", "", URL.pattern.upper()))
		    service_handle_parms=re.sub(r'(?i)'+URL.pattern, "", self.parsed_path.path)
		    print "\t!"+service_handle_value
		    print "\t+"+service_handle_parms
		    break
	    # Llamamos a la funcion que se llame svc_hndl_$(PATRON)
	    #service_handle(service_handle_value)

	    if service_handle_value != "NOOP":
		self.ServiceHandle[service_handle_value](self,service_handle_parms)
	    #self.service_selector(service_handle_value)
		#self.LocalServices.index(URL.pattern)
			      
		#for URL in self.LocalServices:	    
		#    print URL.pattern,'->',URL.match(self.parsed_path.path)
		#if (self.parsed_path.path)
		      
	    content = "<HTML><BODY><PRE>"+self.dump()+"</PRE></BODY></HTML>\n"
	    self.bodySize = len(content)
	    self.do_HEAD()

	    
            self.wfile.write(content)
	    print '_ src: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tSRV: '+self.path
	    
	# Tratamos la peticion como PROXY    
	else:
	    # Está autenticado?
	    self.Allowed = self.handle_PROXY_AUTH()
	    
	    # SI
	    if self.Allowed == 1:
		self.do_HEAD()
		# TODO:: AQUI TENEMOS QUE GESTIONAR EL USUARIO CONTRA LA BBDD
	    # NO, 
	    else:
		self.do_HEAD_AUTH()	    
		
	    print '_ src: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tPRX: '+self.path
	    
        return

    def do_PUSH(self):
        ###self.parse()
        self.do_HEAD()
        self.wfile.write("<HTML><BODY><CODE>"+self.dump()+"</CODE></BODY></HTML>")
        return

