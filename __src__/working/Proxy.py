#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

from __future__ import unicode_literals
import urlparse, base64, binascii, re, string
import BaseHTTPServer
from requests import *
import requests
#import (
#    RequestException, Timeout, URLRequired,
#    TooManyRedirects, HTTPError, ConnectionError
#)
from BaseHTTPServer import BaseHTTPRequestHandler
from pprint import pprint

DEBUG = False

class Proxy(BaseHTTPRequestHandler):
    threadServer = None
    __version__ = '0.1'
    server_version = "HTTP_Proxy/" + __version__
    realm = 'Basic realm="'+server_version+' Authentication required"'
    user = 'none'
    bodySize = None
    password= ''
    Allowed = 0

    
   
    def send_html_message(self, what):
	content = "<HTML><BODY><H1>"+what+"</H1></BODY></HTML>\n"
	self.bodySize = len(content)
	self.do_HEAD()
	self.wfile.write(content)
	return

    def svc_hndl_STOP(self,parms):
	print "svc_hndl_STOP called with parms:"+parms
	self.send_html_message("FORCED SHUTDOWN")
	Proxy.threadServer.force_shutdown()
	return
    
    def svc_hndl_CONFIG(self,parms):
	print "svc_hndl_CONFIG called with parms:"+parms
	self.send_html_message("CONFIG")
	return
    
    def svc_hndl_NOOP(self,parms):
	print "svc_hndl_NOOP called with parms:"+parms
	self.send_html_message("NOOP")
	return

    LocalServices = {
	    re.compile(r"/STOP/", re.IGNORECASE),
	    re.compile(r"/CONFIG/", re.IGNORECASE),
	    re.compile(r"/NOOP/", re.IGNORECASE)
    }
	
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
        #self.send_header('Via', self.server_version)
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
	
	# TODO:: DESCOMENTAR
	### selfquery = False
	# TODO:: DESCOMENTAR

	# Si es una dirección local, atendemos la petición HTTP
	if selfquery:
	    print '_gsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tSRV: '+self.path
	    if DEBUG: pprint(self.parsed_path)

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
	   
	    
	# Tratamos la peticion como PROXY    
	else:
	    # Está autenticado?
	    # TODO:: DESCOMENTAR
	    #self.Allowed = self.handle_PROXY_AUTH()
	    self.Allowed = 1
	    # TODO:: DESCOMENTAR
	    # SI
	    print '_Gsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tPRX: '+self.path
	    if self.Allowed == 1:
		
		if DEBUG:
		    for h in self.headers:
			print "\t.c >"+h.capitalize()+': '+self.headers.dict[h]+"<"
		    #self.send_header(h.capitalize(),resp.headers[h])
		
		try:
		    if DEBUG: print 'try'
		    resp = requests.get(self.path, stream=True)
		    
		except Timeout:
		    print 'exception Timeout'
		    self.send_response(504)
		    self.end_headers()
		except ConnectionError:
		    print 'exception Connection'
		    self.send_response(504)
		    self.end_headers()		    
		else:
		    #if DEBUG: print 'else'
		    if DEBUG: pprint(vars(resp))
		    if  (resp.status_code == requests.codes.ok):
			self.send_response(200)
		    
		    for k, v in resp.headers.items():
			
			if (k == 'date'):
			    pass
			elif (k == 'server'):
			    pass
			elif (k == 'set-cookie'):
			    from requests.cookies import get_cookie_header
			    #pprint(resp.cookies)
			    #pprint(vars(self.request ))
			    #pprint(vars(self.rfile))
			    #pprint(vars(self.server))
			    #print self.dump()
			    #pprint(self.parsed_path)
			    
			    #print k,v
			    POS = [len(v)]
			    for key in resp.cookies.keys():
				POS.append(string.find(v, key+'='))
				
			    POS.sort()
			    print POS
			    print v
			    for i in range(0, len(POS)-1):
				#print i,POS[i],i+1,POS[i+1]
				print v[POS[i]:POS[i+1]]
				
				>>> t = [1, 2, 3, 1, 2, 5, 6, 7, 8]
				>>> t
				[1, 2, 3, 1, 2, 5, 6, 7, 8]
				>>> list(set(t))
				[1, 2, 3, 5, 6, 7, 8]
				>>> s = [1, 2, 3]
				>>> list(set(t) - set(s))
				[8, 5, 6, 7]				
			    #print resp.cookies.items()
			    
			    #beg=-1
			    #for cookie in resp.cookies.keys():
			    #if beg==-1:
				#    beq=resp.cookies.values()
				    
				#print cookie,resp.cookies.get(cookie)
				
			    #a = requests.cookies.RequestsCookieJar
			    #pprint(get_cookie_header(resp.cookies,resp).__expr__)
			    #pprint(extract_cookies_to_jar(resp.cookies, self.path, resp))
			    #key=resp.cookies.keys()
			    #print resp.cookies._find_no_duplicates(key[1])
			    #print "Set-cookie: %s=%s" % (k1, v1)
			    '''
			    for cookie in cookies:
				print "Set-cookie: %s=%s" % (cookie, str(cookies[cookie]))
				print "\t>c %s" % v
				print "\t>s %s" % str(cookie)
				print "\t>.%s: %s." % (k.capitalize(), cookie )
			    '''


			    pass
			elif (k == 'transfer-encoding'):
			    pass
			elif (k=='content-encoding'):
			    pass
			else:
			    #print "\t.%s: %s." % (k.capitalize(), v)
			    self.send_header(k.capitalize(),v)
		    #for h in resp.headers:
		    #if resp.headers[h].count
		    #print "\t."+h.capitalize()+':'+resp.headers[h]
			
			
		    '''
		    for h in resp.headers:
			if (h=='content-encoding'):	    # Requests hace decodificacion transparente, no añadimos la cabecera
			    pass
			elif (h=='transfer-encoding'):	    # Requests hace decodificacion transparente, no añadimos la cabecera
			    pass
			elif (h=='server'):		    # cabecera enviada automaticamente por self.send_response del proxy
			    pass
			elif (h=='date'):		    # cabecera enviada automaticamente por self.send_response del proxy
			    pass
			else:
			    if DEBUG: print "\t."+h.capitalize()+':'+resp.headers[h]
			    self.send_header(h.capitalize(),resp.headers[h])
			#self.send_header(h.capitalize(),resp.headers[h])
			
			self.end_headers()
		    '''
		    self.end_headers()
		    self.wfile.write(resp.content)
		self.wfile.close()
		    
			
	    # NO, 
	    else:
		self.do_HEAD_AUTH()	    
	if DEBUG: print "end"
        return

    def do_POST(self):
	print '_Osrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tPRX: '+self.path
	self.send_response(405)
	self.send_header('Allow','GET, HEAD, PUT')
	self.end_headers
	return
    
    def do_CONNECT(self):
	print '_Csrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tPRX: '+self.path
	self.send_response(405)
	self.send_header('Allow','GET, HEAD, PUT')
	self.end_headers	
	return