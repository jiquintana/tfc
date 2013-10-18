#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

#from __future__ import unicode_literals
import sys
if sys.version_info < (3, 0):
    python_OldVersion = True
else:
    python_OldVersion = False



if python_OldVersion:       # Python version 2.7
    import urlparse, BaseHTTPServer
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SocketServer import BaseRequestHandler
else:                       # Python version 3.x
    import urllib, http.server
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from socketserver import BaseRequestHandler 

import base64, binascii, re, string
import socket

# tenemos que instalar la libreria 'requests' procedente de pip: 
# pip install requests

from requests import *
import requests
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
    parsed_path =''

        
        # http://bugs.python.org/issue14574
        # Versions:	Python 3.4, Python 3.3, Python 3.2, Python 2.7
        # Title:	SocketServer doesn't handle client disconnects properly
    

    def send_html_message(self, what):
        content = "<HTML><BODY><H1>"+what+"</H1></BODY></HTML>\n"
        self.bodySize = len(content)
        self.do_HEAD()
        try:
            #print ('tamagno %s - %s ' % (self.client_address[1],len(resp.content)))
            self.wfile.write(bytes(content, 'UTF-8'))
        except ConnectionAbortedError:
            pass        
        
        return
    
    def send_post(self,content):
        self.bodySize = len(content)
        self.do_HEAD()
        try:
            #print ('tamagno %s - %s ' % (self.client_address[1],len(resp.content)))
            self.wfile.write(bytes(content, 'UTF-8'))        
        except ConnectionAbortedError:
            pass        
        
        return

    def svc_hndl_STOP(self,parms):
        print ("svc_hndl_STOP called with parms: %s" % parms)
        self.send_html_message("FORCED SHUTDOWN")
        Proxy.threadServer.force_shutdown()
        return

    def svc_hndl_CONFIG(self,parms):
        print ("svc_hndl_CONFIG called with parms: %s" % parms)
        self.send_html_message("CONFIG")
        return
    
    def svc_hndl_POST(self,parms):
        print ("svc_hndl_POST called with parms: %s" % parms)
        self.send_post('<html><head><title>My Page</title></head><body><form name="myform" action="/test.php" method="POST"><div align="center"><br><br><input type="text" size="25" value="Enter your name here!"><br><input type="submit" value="Send me your name!"><br></div></form></body></html>')
        return

    def svc_hndl_NOOP(self,parms):
        print ("svc_hndl_NOOP called with parms: %s" % parms)
        self.send_html_message("NOOP")
        return

    LocalServices = {
        re.compile(r"/STOP/",   re.IGNORECASE),
        re.compile(r"/CONFIG/", re.IGNORECASE),
        re.compile(r"/POST/",   re.IGNORECASE),
        re.compile(r"/NOOP/",   re.IGNORECASE)
    }

    ServiceHandle = {
        "STOP": svc_hndl_STOP,
        "CONFIG": svc_hndl_CONFIG,
        "POST": svc_hndl_POST,
        "NOOP": svc_hndl_NOOP
    }    



    '''
    def log_request(self, code='-', size='-'):
	#self.parse_query()
	#pprint(self.dump())
        """Log an accepted request.
           This is called by send_response().

     '''  

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client ip address and current date/time are prefixed to every
        message.

        """

        sys.stderr.write(".%s:%s - - [%s] %s\n" %
                         (self.client_address[0],
                          self.client_address[1],
                          self.log_date_time_string(),
                          format%args))
        
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

        message = '\n'.join([
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                                        self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
        ])

        return message

    def parse_query(self):
        # TODO python 2.7 self.parsed_path = par (urllibn(self.path))
        
        
        if python_OldVersion:
            self.parsed_path = urlparse.urlparse(self.path)
        else:
            #self.path = urllib.parse.unquote(self.path)
            self.parsed_path = urllib.parse.urlparse(self.path)

        

        #print self.log_request.code


        #      'method: '+self.headers.get('path')

        #pprint((vars(self)),indent=8,depth=2)
        #pprint(object, stream=None, indent=1, width=80, depth=None)


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


    def BASIC(self,what):
        if (what==None):
            self.what='GET'     
        else:
            self.what=what
       
        
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
        selfquery = False
        # TODO:: DESCOMENTAR

        # Si es una dirección local, atendemos la petición HTTP
        if selfquery:
            #print '_gsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tSRV: '+self.path
            if DEBUG: pprint(self.parsed_path)

            service_handle_value="NOOP"
            for URL in self.LocalServices:

                print ("\tm%s" % URL.pattern)
                if URL.match(self.parsed_path.path):
                    #print re.sub(URL.pattern.upper())
                    # Sustituimos el patron entre "/" y hacemos strip de los caracteres adicionales

                    service_handle_value=re.sub(r"/[.]*$","",re.sub(r"^/+", "", URL.pattern.upper()))
                    service_handle_parms=re.sub(r'(?i)'+URL.pattern, "", self.parsed_path.path)
                    print ("\t!%s" % service_handle_value)
                    print ("\t+%s" % service_handle_parms)
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

            self.parse_query()
            content = '<HTML><H1>test</H1></HTML>'
            self.bodySize = len(content)
            try:
                #print ('tamagno %s - %s ' % (self.client_address[1],len(resp.content)))
                self.wfile.write(bytes(content, 'UTF-8'))

            except ConnectionAbortedError:
                pass            


        # Tratamos la peticion como PROXY    
        else:
            # Está autenticado?
            # TODO:: DESCOMENTAR
            #self.Allowed = self.handle_PROXY_AUTH()
            self.Allowed = 1
            # TODO:: DESCOMENTAR
            # SI
            #print '_Gsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tPRX: '+self.path
            if self.Allowed == 1:

                if DEBUG:
                    for h in self.headers:
                        print ("\t.c >%s: %s<" % (h.capitalize(),self.headers[h]))
                    #self.send_header(h.capitalize(),resp.headers[h])

                try:
                    if DEBUG: print('URL: %s: %s' % (self.client_address[1],self.path))
                    if DEBUG: print ('try')
                    if ( self.what == 'GET' ):
                        resp = requests.get(self.path, stream=True, allow_redirects=True)
                    elif ( self.what == 'POST' ):
                        resp = requests.post(self.path, stream=True, allow_redirects=True)
                    #print (resp.history)
                    #print (len(resp.content))

                except Timeout:
                    print ('exception Timeout')
                    self.send_response(504)
                    self.end_headers()
                except ConnectionError:
                    print ('exception Connection')
                    self.send_response(504)
                    self.end_headers()		    
                else:
                    if DEBUG: print('else')
                    if DEBUG: pprint(vars(resp))
                    if  (resp.status_code == requests.codes.ok):
                        self.send_response(resp.status_code)
                    
                    # Control de la cabecera via
                    via_header_seen = False
                    
                    for k, v in resp.headers.items():
                        if DEBUG: print('IN header: %s - %s: %s' % (self.client_address[1],k.capitalize(),v))
                        if (k == 'date'):
                            pass
                        elif (k== 'content-length'):
                            # Debido a que la librería request hace descompresion automatica, no nos podemos
                            # fiar del valor 'content-length' en caso de codificacion deflate/gzip, asi que
                            # reescribimos la cabecera incondicionalmente
                            self.send_header(k.capitalize(), len(resp.content))
                            if DEBUG:
                                print('OU header CL: %s - %s: %s' % (self.client_address[1],k.capitalize(),v))
                                print('OU header SZ: %s -   : %s' % (self.client_address[1], len(resp.content)))
                            pass
                        elif (k == 'transfer-encoding'):
                            # Eliminamos transfer-encoding por la misma razon anterior 
                            pass
                        elif (k=='content-encoding'):
                            # Eliminamos transfer-encoding por la misma razon anterior
                            pass                        
                        elif (k== 'via'):
                            via_header_seen = True
                            # Agnadimos a cabecera via
                            v+=', http/1.0 '+self.server_version
                            self.send_header(k.capitalize(),v)
                            #print('OU header: %s - %s: %s' % (self.client_address[1],k.capitalize(),v))                            
                            
                        elif (k == 'server'):
                            # la escribe directamente el servidor BaseHTTPServer
                            pass
                        elif (k == 'set-cookie'):

                            from requests.cookies import get_cookie_header			    
                            # Este bloque gestiona las cookies; Requests devuelve todas las cookies en un array 'set-cookie', pero indistinguible si hay varias.
                            # para obtener todos los parámetros y reenviarlos, parseamos la cadena.		
                            def allindices(string, sub, listindex=[], offset=0):
                                i = string.find(sub, offset)
                                while i >= 0:
                                    listindex.append(i)
                                    i = string.find(sub, i + 1)
                                return listindex				    

                            POS = [0,len(v)]
                            for key in resp.cookies.keys():
                                for i in allindices(v, ', '+key+'='): POS.append(i)
                                for i in allindices(v, key+'='): POS.append(i)

                            POS=list(set(POS))
                            POS.sort()
                            # ahora tenemos un array con las posiciones de las cookies a cortar				

                            while (POS != []):
                                parsed_cookie=v[POS[0]:POS[1]]
                                self.send_header('Set-Cookie',parsed_cookie)
                                if DEBUG: 
                                    print ("\t... cookie: Set-cookie=%s" % (v[POS[0]:POS[1]]))
                                #eliminamos las posisiones 0 y 1; como eliminamos primero el valor [0], el valor [1] se vuelve [0] en el siguiente desapilado
                                POS.remove(POS[0])
                                POS.remove(POS[0])
                            pass
                           
                        
                    
                        else:
                            if DEBUG: print('OU header: %s - %s: %s' % (self.client_address[1],k.capitalize(),v))                            
                            self.send_header(k.capitalize(),v)
                            #print(resp.content)
                            
                    if (not via_header_seen):
                        # Agnadimos a cabecera via
                        k='Via'
                        v='http/1.0 '+self.server_version
                        self.send_header(k.capitalize(),v)
                        if DEBUG: print('OU header: %s - %s: %s' % (self.client_address[1],k.capitalize(),v))                            
                    
                    self.end_headers()

                    try:
                        #print ('tamagno %s - %s ' % (self.client_address[1],len(resp.content)))
                        self.wfile.write(resp.content)                     
                    except ConnectionAbortedError:
                        pass
            # NO, 
            else:
                self.do_HEAD_AUTH()	    
        if DEBUG: print ("end")
        return

    def do_GET(self):
        self.BASIC(what='GET')
        return
    
    def do_POST(self):
        #print '_Osrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tPRX: '+self.path
        self.BASIC(what='POST')
        '''
        self.send_response(405)
        self.send_header('Allow','GET, HEAD, PUT')
        self.end_headers
        '''
        return

    def do_CONNECT(self):
        #print '_Csrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tUSR: '+self.user+',\tPRX: '+self.path
        self.send_response(405)
        self.send_header('Allow','GET, HEAD, PUT')
        self.end_headers	
        return