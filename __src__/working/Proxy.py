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
import socket, select, os
import cgi

#import logging
#import http.client



# tenemos que instalar la libreria 'requests' procedente de pip: 
# pip install requests

from requests import *
import requests
import Headers
import Cache
from Log import Log
#import Log

DEBUG_LEVELS = ['CONNECTIONS','HEADERS', 'AUTH']
DEBUG = False

class Proxy(BaseHTTPRequestHandler):
    threadServer = None
    __version__ = '0.1'
    server_version = "HTTP_Proxy/" + __version__
    proxy_user = 'xxxxxxxxx'
    proxy_password = ''
    http_user = 'xxxxxxxxx'
    http_password = ''
    bodySize = None
    Allowed = 0
    parsed_path =''
    content = b''
    content_lenght = 0
    processed_headers = []
    code = 0
    content_cached=False
    logger = Log()

    #http.client.HTTPConnection.debuglevel = 1

    #logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
    #logging.getLogger().setLevel(logging.DEBUG)
    #requests_log = logging.getLogger("requests.packages.urllib3")
    #requests_log.setLevel(logging.DEBUG)
    #requests_log.propagate = True


    __verbs_supported ='GET, HEAD, POST, PUT, TRACE, OPTIONS, CONNECT'
    __verbs_unsupported = 'PATCH, DELETE'
    __verbs_safe = 'GET, HEAD, OPTIONS, TRACE'


    # http://bugs.python.org/issue14574
    # Versions:	Python 3.4, Python 3.3, Python 3.2, Python 2.7
    # Title:	SocketServer doesn't handle client disconnects properly
    
    '''    def get_timestamp(self, timestamp=None):
            if timestamp is None:
                timestamp = time.time()
            year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
            s = "%04d.%2d.%2d %02d:%02d:%02d" % (
                year, month, day, 
                hh, mm, ss)
            return s	
    '''
    def __init__(self, request, client_address, server):
        if not python_OldVersion:
            super().__init__(request, client_address, server)   
        else:
            BaseHTTPRequestHandler.__init__(self, request, client_address, server)
            
        self.content = b''
        self.content_lenght = 0
        self.code = 0
        self.processed_headers [:] = []
        self.content_cached=False 
        self.Allowed = 0
        
    def log_message(self, format, *args):
        return
    '''
        def pdebug(self,message):
            if TRACE:
                if len(message) > MAX_CON_MSG:
                    sys.stderr.write('%s - %s\n' % (self.get_timestamp(), message[0:MAX_CON_MSG-3]+'..'))
                else:
                    sys.stderr.write('%s - %s\n' % (self.get_timestamp(), message))
            return
    '''

    def svc_hndl_FILE(self,parms,query, Verb=''):
        self.logger.pdebug("svc_hndl_FILE called with parms: >%s, %s<" % (Verb, parms))

        if Verb=='HEAD':
            mensaje=''
        else:    
            if DEBUG: self.logger.pdebug("url parms = %s, %s" % (parms,query))
            filename=re.sub(r'[^a-zA-Z0-9]', "", parms).lower()

            if os.path.exists('./static/'+filename+'.static'):
                source = open('./static/'+filename+'.static', 'r')
                mensaje = source.read()
                self.int_send_HEADERS(200,mensaje)

            else:
                mensaje=self.int_get_html_message('File "<font color="red">'+filename+'</font>" not found')
                self.int_send_HEADERS(404,mensaje)
                #self.int_send_BODY(mensaje)

        if Verb!='HEAD':
            self.int_send_BODY(mensaje)


        return

    def svc_hndl_STOP(self,parms,query, Verb=''):
        self.logger.pdebug("svc_hndl_STOP called with parms: >%s, %s<" % (Verb, parms))
        if Verb=='HEAD':
            mensaje=''
        else:
            mensaje=self.int_get_html_message('STOP hndl')

        self.int_send_HEADERS(200,mensaje)

        if Verb!='HEAD':
            self.int_send_BODY(mensaje)
            Proxy.threadServer.force_shutdown()

        #self.send_html_message("FORCED SHUTDOWN")
        return

    def svc_hndl_CONFIG(self,parms,query, Verb=''):
        self.logger.pdebug("svc_hndl_CONFIG called with parms: >%s, %s<" % (Verb, parms))
        if Verb=='HEAD':
            mensaje=''
        else:
            mensaje=self.int_get_html_message('CONFIG hndl')
        self.int_send_HEADERS(200,mensaje)

        if Verb!='HEAD':
            self.int_send_BODY(mensaje)


        #self.send_html_message("CONFIG")
        return

    def svc_hndl_POST(self,parms,query, Verb=''):
        self.logger.pdebug("svc_hndl_POST called with parms: >%s, %s<" % (Verb, parms))
        if Verb=='HEAD':
            mensaje=''
        else:
            mensaje='<html><head><title>My Page</title></head><body><form name="myform" action="http://localhost/dump.php" method="POST"><div align="center"><br><br><input type="text" size="25" value="Enter your name here!"><br><input type="submit" value="Send me your name!"><br></div></form></body></html>'
            self.int_send_HEADERS(200,mensaje)

        if Verb!='HEAD':
            self.int_send_BODY(mensaje)

        return

    def svc_hndl_NOOP(self,parms,query, Verb=''):
        self.logger.pdebug("svc_hndl_NOOP called with parms: >%s, %s<" % (Verb, parms))
        if Verb=='HEAD':
            mensaje=''
        else:
            mensaje=self.int_get_html_message('NOOP hndl')
        self.int_send_HEADERS(200,mensaje)

        if Verb!='HEAD':
            self.int_send_BODY(mensaje)

        return


    LocalServices = {
        re.compile(r"/STOP/",   re.IGNORECASE),
        re.compile(r"/CONFIG/", re.IGNORECASE),
        re.compile(r"/POST/",   re.IGNORECASE),
        re.compile(r"/FILE/",   re.IGNORECASE),
        re.compile(r"/NOOP/",   re.IGNORECASE)
    }

    ServiceHandle = {
        "STOP": svc_hndl_STOP,
        "CONFIG": svc_hndl_CONFIG,
        "POST": svc_hndl_POST,
        "FILE": svc_hndl_FILE,
        "NOOP": svc_hndl_NOOP
    }    


    def int_get_html_message(self, what):
        content = "<HTML><BODY><H1>"+what+"</H1></BODY></HTML>\n"
        return content    

    def int_send_HEADERS(self, code=200, message=''):
        if message != '':
            self.bodySize=len(message)
        self.send_response(code)
        self.send_header('Content-Type', 'text/html;charset=UTF-8')
        self.send_header('Content-Length', self.bodySize)	
        self.end_headers()
        return

    def int_send_BODY(self, message=''):
        try:
            if python_OldVersion:
                self.wfile.write(message)
            else:
                self.wfile.write(bytes(message, 'UTF-8'))        

        except:
            self.logger.pdebug('excepcion en send_body :%s, %s' % (self.what, self.path))

            pass

        return

    def int_HEAD_PROXY_AUTH(self):
        self.send_response(407,"Proxy Authentication Required. "+self.server_version+": Access to the Web Proxy filter is denied.")
        #self.send_header('Proxy-Authenticate', 'Negotiate')
        self.send_header('Proxy-Authenticate', 'Basic realm="PROXY autentication required"')
        #self.send_header('Via', self.server_version)
        self.send_header('Proxy-Connection', 'close')
        self.send_header('Connection', 'close')
        self.end_headers()
        return

    def int_HEAD_HTTP_AUTH(self):
        self.send_response(401,"HTTP authentication Required. "+self.server_version+": Access to the Web Server is denied.")
        #self.send_header('WWW-Authenticate', 'Negotiate')
        self.send_header('WWW-Authenticate', 'Basic realm="HTTP autentication required"')
        #self.send_header('Via', self.server_version)
        self.send_header('Connection', 'close')
        self.end_headers()
        return

    def parse_query(self):
        if python_OldVersion:
            self.parsed_path = urlparse.urlparse(self.path)
        else:
            self.parsed_path = urllib.parse.urlparse(self.path)
        return

    #TODO: Proxy-Authorization: Basic dXNlcjpwYXNzd29yZA==
    #TODO: dividir en 407 (proxy) y Authentication http

    def handle_PROXY_AUTH(self):

        # Tenemos una cabecera con autenticacion Proxy?

        ## Python 3 => removed self.headers.>has_key<('Proxy-Authorization'):
        ## cambiado por 'in'
        if 'Proxy-Authorization' in self.headers:

            authorization = self.headers.get('Proxy-Authorization')

            if DEBUG: self.logger.pdebug ('Proxy auth string [Proxy-Authorization]: %s ' % authorization)

            authorization = authorization.split()
            # Han usado una autenticación básica?
            if authorization[0].lower() == "basic":
                try:
                    # Sí, intentamos obtener el usuario y passwd
                    if python_OldVersion:
                        authorization = base64.decodestring(authorization[1])
                    else:
                        authorization = base64.decodestring(bytes(authorization[1],'UTF-8')).decode()
                    # bytes(content, 'UTF-8')

                except binascii.Error:
                    # Error, entonces KO
                    return 0 

                else:
                    # Tenemos usuario & paswd y lo hemos podido decodificar
                    authorization = authorization.split(':')
                    self.proxy_user=authorization[0]
                    self.proxy_password=authorization[1]
                    if self.proxy_user == 'proxyUser' and self.proxy_password == 'proxyPass':
                        #Autenticacion = OK
                        return 1
                    else:
                        #Autenticacion = KO
                        return 0	    

        # No está autenticado
        else:
            return 0

    def handle_HTTP_AUTH(self):

        # Tenemos una cabecera con autenticacion Proxy?

        ## Python 3 => removed self.headers.>has_key<('Authorization'):
        ## cambiado por 'in'

        if 'Authorization' in self.headers:
            authorization = self.headers.get('Authorization')

            if DEBUG: self.logger.pdebug ('HTTP auth string [Authorization]: %s ' % authorization)

            authorization = authorization.split()

            # Han usado una autenticación básica?
            if authorization[0].lower() == "basic":
                try:
                    # Sí, intentamos obtener el usuario y passwd
                    #authorization = base64.decodestring(authorization[1])

                    if python_OldVersion:
                        authorization = base64.decodestring(authorization[1])
                    else:
                        authorization = base64.decodestring(bytes(authorization[1],'UTF-8')).decode()
                    # bytes(content, 'UTF-8')                    

                except binascii.Error:
                    # Error, entonces KO
                    return 0 

                else:
                    # Tenemos usuario & paswd y lo hemos podido decodificar
                    authorization = authorization.split(':')
                    self.http_user=authorization[0]
                    self.http_password=authorization[1]
                    if self.http_user == 'User' and self.http_password == 'Pass':
                        #Autenticacion = OK
                        return 1
                    else:
                        #Autenticacion = KO
                        return 0	    

        # No está autenticado
        else:
            return 0


    def BASIC(self,what):
        self.content = b''
        self.content_lenght = 0
        self.code = 0
        self.processed_headers [:] = []
        #self.processed_headers.clear()
        self.content_cached=False 
        self.Allowed = 0
        
        if (what==None):
            self.what='GET'
        else:
            self.what=what


        self.parse_query()
        # Comprobamos si nos están pidiendo nuestra URL
        # Por defecto no nos piden a nosotros
        selfquery = False

        ## TODO: aqui hay que cambiar que empiece por la cadena en vez de que sea la cadena
        ## TODO: cuando atacamos localhost:PUERTO (modo proxy), devuelve OK, pero cuando se ataca el servicio
        ## TODO: sin puerto, se devuelve como contenido las cabeceras
        if self.parsed_path.netloc in [ '127.0.0.1' , 'localhost', '' ]:
            # or '' ]
            selfquery = True;

        # TODO:: DESCOMENTAR
        ## La siguiente linea fuerza el uso de modo proxy
        ## selfquery = False
        # TODO:: DESCOMENTAR


        # Si es una dirección local, atendemos la petición HTTP
        #######################################################
        if selfquery:
            if DEBUG:
                self.logger.pdebug(self.parsed_path)
                self.logger.pdebug("Local, %s %s" % (selfquery, self.what))


            self.Allowed = self.handle_HTTP_AUTH()
            if DEBUG: self.logger.pdebug("autorizado by HTTP_AUTH: %s " % self.Allowed)
            if self.Allowed==1:
                # handler por defecto... 
                service_handle_value="NOOP"
                service_handle_parms=""

                self.logger.pdebug("self.what: %s " % self.what)
                if self.what in ['GET', 'POST', 'HEAD']:
                    # Para cada uno de los servicios que atenderemos... (LocalServices es una lista de servicios vs handlers)
                    for URL in self.LocalServices:
                        if DEBUG: self.logger.pdebug ("\tm%s" % URL.pattern)
                        if URL.match(self.parsed_path.path):

                            # Sustituimos el patron entre "/" y hacemos strip de los caracteres adicionales
                            service_handle_value=re.sub(r"/[.]*$","",re.sub(r"^/+", "", URL.pattern.upper()))
                            service_handle_parms=re.sub(r'(?i)'+URL.pattern, "", self.parsed_path.path)

                    # Llamamos a la funcion que se llame svc_hndl_$(PATRON)
                    # Por defecto, se llama a la funcion NOOP

                    self.ServiceHandle[service_handle_value](self,service_handle_parms,self.parsed_path.query,Verb=self.what)
                    service_handle_value = 'NOOP'

                else:
                    self.do_OTHER()
            else:
                self.int_HEAD_HTTP_AUTH()



        # Tratamos la peticion como PROXY
        # ######################################################
        else:
            if DEBUG: self.logger.pdebug(self.parsed_path)

            # Está autenticado?
            # Habilitamos la autenticacion o forzamos autenticado..
            # TODO:: DESCOMENTAR
            self.Allowed = self.handle_PROXY_AUTH()

            if DEBUG: self.logger.pdebug("autorizado by PROXY_AUTH: %s " % self.Allowed)

            #self.Allowed = 1
            # TODO:: DESCOMENTAR

            if self.Allowed == 1:
                self.client_headers = {}
                self.client_headers.clear()
                
                client_headers = Headers.ClientHeaders(self.headers.__str__(),debug=False,
                                                                      ip=self.client_address[0],
                                                                      port = self.client_address[1])                
                new_client_headers,client_cookies = client_headers.parse()

                if DEBUG: self.logger.pdebug('URL: %s: %s' % (self.client_address[1],self.path))
                if DEBUG: self.logger.pdebug ('try request')
                
                fc = Cache.FileCache()
                # Filtramos el tipo de servicio y llamamos a un bloque o a otro...
                if ( self.what == 'GET' ):
                    
                    cache_content = b''
                    cache_headers = []
                    cache_headers[:] = []
                    #cache_headers.clear()
                    self.content_cached = fc.is_cached(path=self.path, debug=False, ip=self.client_address[0], port=self.client_address[1])
                    if self.content_cached:
                        cache_content, cache_headers = fc.get(path=self.path, debug=True, ip=self.client_address[0], port=self.client_address[1])
                        cache_lenght = len(cache_content)
                        cache_code = 200
                    else:
                        resp = requests.get(self.path, headers=new_client_headers, stream=True, allow_redirects=True)
                        #fc.put(path=self.path, content=resp.content, headers=resp.headers, debug=True, ip=self.client_address[0], port=self.client_address[1])
                elif ( self.what == 'POST' ):
                    resp = requests.post(self.path, headers=new_client_headers, data=self.content, stream=True, allow_redirects=True)
                elif ( self.what == 'HEAD' ):
                    resp = requests.head(self.path, stream=True, allow_redirects=True)
               
                if self.content_cached:
                    self.content = bytes(cache_content)
                    self.content_lenght = cache_lenght
                    self.code = cache_code                        
                else:
                    self.content = resp.content
                    self.content_lenght = len(resp.content)
                    self.code = resp.status_code

                
                if  (self.code == requests.codes.ok):
                    # enviamos el codigo
                    self.send_response(self.code)
                    self.processed_headers [:] = []
                    #self.processed_headers.clear()
                    parsed_headers = []
                    parsed_headers [:] = []
                    could_cache=True
                    if not self.content_cached:                        
                        # Procesamos las cabeceras para reescribirlas
                        '''if 'pragma' in resp.headers and resp.headers['pragma'] == 'no-cache':
                            #print('Cache header: pragma ->%s' % resp.headers['pragma'])
                            could_cache=False
                        elif 'expires' in resp.headers and resp.headers['expires'] == '-1':
                            #print('Cache header: expires ->%s' % resp.headers['expires'])
                            could_cache=False   
                        #elif 'cache-control' in resp.headers:
                            #print('\tCache header: cache-control ->%s' % resp.headers['cache-control'])
                            #could_cache=False
                        '''
                        parsed_headers = Headers.ServerHeaders(response=resp, debug=False, 
                                                 ip=self.client_address[0],
                                                 port = self.client_address[1])
                        self.processed_headers = parsed_headers.parsed_headers()
                      
                        if could_cache:
                            fc.put(path=self.path, content=resp.content, headers=self.processed_headers, debug=False, ip=self.client_address[0], port=self.client_address[1])
                    else:
                        for header in cache_headers:
                            header_key,header_value = str(header).split(': ',1)
                            self.processed_headers.append([header_key,header_value])
                    
                    
                    # Enviamos todas las cabeceras reescritas
                    for header_key,header_value in self.processed_headers:
                        self.send_header(header_key, str(header_value).rstrip('\n'))
                    
                    
                    # Fin de cabeceras
                    self.end_headers()
                    
                    if self.what != 'HEAD' and self.code==200:
                        self.wfile.write(self.content)
                        
            else:
                self.int_HEAD_PROXY_AUTH()
        if DEBUG: self.logger.pdebug ("end")
        return

    def do_CONNECT(self):
        o_port_default = None
        o_port = 80

        self.parse_query()
        if DEBUG:
            self.logger.pdebug (self.parsed_path)
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    '??? CNT '+ self.path)
        # Tenemos schema? => eso nos fija el puerto por defecto en caso de no
        # venir definido en la cadena CONNECT...
        if self.parsed_path.scheme != '':
            o_port_default = socket.getservbyname(self.parsed_path.scheme)

        destination = self.parsed_path.netloc if (self.parsed_path.netloc!='') else self.parsed_path.path

        try:
            o_dest,o_port = destination.split(':', 1)
        except:
            o_dest = destination
            if (o_port_default!=None): o_port=o_port_default

        try:
            if DEBUG: self.logger.pdebug ('Outbound conection to %s:%s' % (o_dest, o_port))
            self.server_socket = socket.create_connection((o_dest, o_port),timeout=3)

        except (socket.error, socket.herror, socket.gaierror) as e:
            if DEBUG: self.logger.pdebug ("Error %s" % e)
            self.send_response(404,'CONNECT error ['+str(e)+'] to '+o_dest+':'+str(o_port))
            self.end_headers()              

        except socket.timeout as e:
            if DEBUG: self.logger.pdebug ("Error %s" % e)
            self.send_response(504,'CONNECT Timeout ['+str(e)+'] to '+o_dest+':'+str(o_port))
            #self.send_header('Content-Length', '0')
            self.end_headers()            

        else:      
            self.send_response(200,'CONNECT OK -> '+o_dest+':'+str(o_port))
            self.send_header('Content-Length', '0')
            self.end_headers() 

            self.server_wfile = self.server_socket.makefile('wb', self.wbufsize)            

            #self.logger.pdebug('_Csrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)		
            self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                        'Allow: %s, ' % self.Allowed +
                        'prxUSR: %10s, ' % self.proxy_user[0:9] +
                        'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                        'PRX CNT '+ self.path)
            salir_bucle = False
            inputs = [self.connection, self.server_socket]            
            while (inputs and not salir_bucle):
                # Wait for at least one of the sockets to be ready for processing

                if DEBUG:
                    sys.stderr.write("waiting for the next event")

                #readable, writable, exceptional = select.select(inputs, [], inputs)
                r, w, e = select.select(inputs, [], inputs)
                if DEBUG:
                    sys.stderr.write("select (i:%s, o:%s, e:%s'%(len(r),len(w),len(e))")

                if e != [] and not salir_bucle:
                    # cualquiera que sea el error en los sockets de cliente o servidor, tenemos que salir..

                    if self.connection in e:
                        if DEBUG: self.logger.pdebug("error socket cliente: cerrandolo")
                    if server_socket in e:
                        if DEBUG: self.logger.pdebug("error socket servidor: cerrandolo")
                    if DEBUG: self.logger.pdebug(e)
                    salir_bucle=True

                if r != [] and not salir_bucle:
                    if DEBUG: self.logger.pdebug(r)
                    if (self.connection in r) and not salir_bucle:
                        if DEBUG: self.logger.pdebug('cliente tiene datos: leyendo cliente')  
                        try:
                            sockdata = self.connection.recv(4096)
                            if (sockdata):
                                self.server_wfile.write(sockdata)
                            else:
                                if DEBUG: self.logger.pdebug("Cierre de socket cliente ordenado")
                                salir_bucle=True   
                        except (socket.timeout, socket.error) as e:
                            if DEBUG: self.logger.pdebug("error socket: %s" % (e))
                            salir_bucle=True   

                    if (self.server_socket in r) and not salir_bucle:
                        if DEBUG: self.logger.pdebug('servidor tiene datos: leyendo servidor')               
                        try:
                            sockdata = self.server_socket.recv(4096)
                            if (sockdata):
                                self.wfile.write(sockdata)
                            else:
                                if DEBUG: self.logger.pdebug("Cierre de socket servidor ordenado")
                                salir_bucle=True
                        except (socket.timeout, socket.error) as e:
                            if DEBUG: self.logger.pdebug("error socket: %s" % (e))
                            salir_bucle=True   

                if w != [] and not salir_bucle:
                    if DEBUG: self.logger.pdebug(w)

        if DEBUG: self.logger.pdebug ("saliendo del bucle del socket...")
        self.server_wfile.close()
        self.server_socket.close()
        return

##     __verbs_supported ='GET, HEAD, POST, PUT, TRACE, OPTIONS, CONNECT'
##                         xxx  xxxx  xxxx              xxxxxxx  xxxxxxx

    def do_OPTIONS(self):
        self.content = ''
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    '??? OPT '+ self.path)        
        if (self.path == '*'):
            self.send_response(200)
            self.send_header('Allow',self.__verbs_supported)
            self.send_header('Content-Length', '0')	
            self.end_headers            
        else:
            self.BASIC(what='OPTIONS')
            # TODO:: OPTIONS de url requiere auth... gesionado en BASIC      
            self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                        'Allow: %s, ' % self.Allowed +
                        'prxUSR: %10s, ' % self.proxy_user[0:9] +
                        'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                        'PRX OPT '+ self.path)
        return    

    def do_HEAD(self):
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    '??? HEA '+ self.path)        
        self.content = ''
        self.BASIC(what='HEAD')
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    'PRX HEA '+ self.path)
        return

    def do_TRACE(self):
        self.content = ''
        self.BASIC(what='TRACE')
        self.logger.pdebug( '%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    'PRX TRC '+ self.path)
        return

    def do_GET(self):
        '''
        parsed_headers = Headers(headers=self.headers.items(), debug=True, 
                                ip=self.client_address[0],
                                port = self.client_address[1])
        returned_headers = parsed_headers.input_parsed_headers()
        '''
        
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    '??? GET %s' % (self.path)
                     )            
        
        if 'Content-Length' in self.headers:
            self.content = self.rfile.read(int(self.headers['Content-Length']))
        else:
            self.content = ''        
        self.BASIC(what='GET')
        '''       
        msg = "%s:%s: " % (self.client_address[0], self.client_address[1])+
                   'Allow: %s, ' % self.Allowed +
                   'prxUSR: %10s, ' % self.proxy_user[0:9] +
                   'Cod: %3d, Size: %8d,' % (self.code, self.content_lenght) +
                   'PRX GET ' + self.path
        '''
        if self.content_cached:
            self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                        'Allow: %s, ' % self.Allowed +
                        'prxUSR: %10s, ' % self.proxy_user[0:9] +
                        'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                        'CAC GET %s' % (self.path)
                        )            
        else:
            self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                        'Allow: %s, ' % self.Allowed +
                        'prxUSR: %10s, ' % self.proxy_user[0:9] +
                        'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                        'PRX GET %s' % (self.path)
                        )
        
        return


    def do_POST(self):
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    '??? PST %s' % (self.path)
                    )   
        
        if 'Content-Length' in self.headers:
            self.content = self.rfile.read(int(self.headers['Content-Length']))
        else:
            self.content = ''

        if DEBUG: sys.stderr.write('calling BASIC\n')
        self.BASIC(what='POST')
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d, ' % (self.code, self.content_lenght) +
                    'PRX PST '+ self.path)
        return


    def do_OTHER(self):
        self.content = ''
        self.send_response(405)
        self.send_header('Allow',self.__verbs_supported)
        self.end_headers
        self.logger.pdebug('%s:%s, ' % (self.client_address[0], self.client_address[1]) +
                    'Allow: %s, ' % self.Allowed +
                    'prxUSR: %10s, ' % self.proxy_user[0:9] +
                    'Cod: %3d, Size: %8d,' % (self.code, self.content_lenght) +
                    'PRX OTH '+ self.path)

        return