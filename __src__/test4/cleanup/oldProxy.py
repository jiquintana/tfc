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
import socket, select, time, os
import cgi

# tenemos que instalar la libreria 'requests' procedente de pip: 
# pip install requests

from requests import *
import requests
from pprint import pprint
from Headers import Headers

DEBUG_LEVELS = ['CONNECTIONS','HEADERS', 'AUTH']
DEBUG = False
TRACE = True
MAX_CON_MSG = 180

class Proxy(BaseHTTPRequestHandler):
    threadServer = None
    __version__ = '0.1'
    server_version = "HTTP_Proxy/" + __version__
    realm = 'Basic realm="'+server_version+' Authentication required"'
    proxy_user = 'none'
    proxy_password = ''
    http_user = 'none'
    http_password = ''
    bodySize = None
    Allowed = 0
    parsed_path =''
    content = ''

    __verbs_supported ='GET, HEAD, POST, PUT, TRACE, OPTIONS, CONNECT'
    __verbs_unsupported = 'PATCH, DELETE'
    __verbs_safe = 'GET, HEAD, OPTIONS, TRACE'


    # http://bugs.python.org/issue14574
    # Versions:	Python 3.4, Python 3.3, Python 3.2, Python 2.7
    # Title:	SocketServer doesn't handle client disconnects properly


    def get_timestamp(self, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
        s = "%04d.%2d.%2d %02d:%02d:%02d" % (
            year, month, day, 
            hh, mm, ss)
        return s	

    def log_message(self, format, *args):
        return

    def pdebug(self,message):
        if TRACE:
            if len(message) > MAX_CON_MSG:
                sys.stderr.write('%s - %s\n' % (self.get_timestamp(), message[0:MAX_CON_MSG-3]+'..'))
            else:
                sys.stderr.write('%s - %s\n' % (self.get_timestamp(), message))
        return


    def svc_hndl_FILE(self,parms,query, Verb=''):
        print ("svc_hndl_FILE called with parms: >%s, %s<" % (Verb, parms))

        if Verb=='HEAD':
            mensaje=''
        else:    
            print("url parms = %s, %s" % (parms,query))
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
        print ("svc_hndl_STOP called with parms: >%s, %s<" % (Verb, parms))
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
        print ("svc_hndl_CONFIG called with parms: >%s, %s<" % (Verb, parms))
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
        print ("svc_hndl_POST called with parms: >%s, %s<" % (Verb, parms))
        if Verb=='HEAD':
            mensaje=''
        else:
            mensaje='<html><head><title>My Page</title></head><body><form name="myform" action="http://localhost/dump.php" method="POST"><div align="center"><br><br><input type="text" size="25" value="Enter your name here!"><br><input type="submit" value="Send me your name!"><br></div></form></body></html>'
            self.int_send_HEADERS(200,mensaje)

        if Verb!='HEAD':
            self.int_send_BODY(mensaje)

        return

    def svc_hndl_NOOP(self,parms,query, Verb=''):
        print ("svc_hndl_NOOP called with parms: >%s, %s<" % (Verb, parms))
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
            print ('excepcion en send_body :%s, %s' % (self.what, self.path))

            pass

        return

    def int_HEAD_PROXY_AUTH(self):
        self.send_response(407,"Proxy Authentication Required. "+self.server_version+": Access to the Web Proxy filter is denied.")
        #self.send_header('Proxy-Authenticate', 'Negotiate')
        self.send_header('Proxy-Authenticate', self.realm)
        #self.send_header('Via', self.server_version)
        self.send_header('Proxy-Connection', 'close')
        self.send_header('Connection', 'close')
        self.end_headers()
        return

    def int_HEAD_HTTP_AUTH(self):
        self.send_response(401,"HTTP authentication Required. "+self.server_version+": Access to the Web Server is denied.")
        #self.send_header('WWW-Authenticate', 'Negotiate')
        self.send_header('WWW-Authenticate', self.realm)
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

            if DEBUG: print ('Proxy auth string [Proxy-Authorization]: %s ' % authorization)

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

            if DEBUG: print ('HTTP auth string [Authorization]: %s ' % authorization)

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
                pprint(self.parsed_path)
                print("Local, %s %s" % (selfquery, self.what))


            self.Allowed = self.handle_HTTP_AUTH()
            if DEBUG: print("autorizado by HTTP_AUTH: %s " % self.Allowed)
            if self.Allowed==1:
                # handler por defecto... 
                service_handle_value="NOOP"
                service_handle_parms=""

                print("self.what: %s " % self.what)
                if self.what in ['GET', 'POST', 'HEAD']:
                    # Para cada uno de los servicios que atenderemos... (LocalServices es una lista de servicios vs handlers)
                    for URL in self.LocalServices:
                        if DEBUG: print ("\tm%s" % URL.pattern)
                        if URL.match(self.parsed_path.path):
                            #print re.sub(URL.pattern.upper())
                            # Sustituimos el patron entre "/" y hacemos strip de los caracteres adicionales

                            service_handle_value=re.sub(r"/[.]*$","",re.sub(r"^/+", "", URL.pattern.upper()))
                            service_handle_parms=re.sub(r'(?i)'+URL.pattern, "", self.parsed_path.path)



                            #break

                    # Llamamos a la funcion que se llame svc_hndl_$(PATRON)
                    # Por defecto, se llama a la funcion NOOP
                    pprint(self.parsed_path, indent=1, depth=80)
                    pprint(object)
                    self.ServiceHandle[service_handle_value](self,service_handle_parms,self.parsed_path.query,Verb=self.what)
                    service_handle_value = 'NOOP'

                else:
                    self.do_OTHER()
            else:
                self.int_HEAD_HTTP_AUTH()



        # Tratamos la peticion como PROXY
        # ######################################################
        else:
            if DEBUG: pprint(self.parsed_path)

            # Está autenticado?
            # Habilitamos la autenticacion o forzamos autenticado..
            # TODO:: DESCOMENTAR
            self.Allowed = self.handle_PROXY_AUTH()

            if DEBUG: print("autorizado by PROXY_AUTH: %s " % self.Allowed)

            #self.Allowed = 1
            # TODO:: DESCOMENTAR

            if self.Allowed == 1:


                self.client_headers = {}
                #print(">>>>>>>>")
                for k,v in self.headers.items():
                    #print('>>>> %s -> %s' %(k,v))
                    if k not in ['Cookie','Proxy-Authorization']: self.client_headers[k]=v

                #print("<<<<<<<<")					
                try:
                    if DEBUG: print('URL: %s: %s' % (self.client_address[1],self.path))
                    if DEBUG: print ('try request')

                    # Si la petición contiene datos...
                    if 'content-length' in self.headers:
                        self.content = self.rfile.read(int(self.headers.getheader('content-length')))
                        if DEBUG: sys.stderr.write('\ncontent'); pprint(self.content)

                    # Filtramos el tipo de servicio y llamamos a un bloque o a otro...
                    if ( self.what == 'GET' ):
                        #pprint(vars(self))
                        resp = requests.get(self.path, stream=True,timeout=5, allow_redirects=True)

                    elif ( self.what == 'POST' ):
                        resp = requests.post(self.path, headers=self.headers,
                                             data=self.content, stream=True, allow_redirects=True)                        
                    elif ( self.what == 'HEAD' ):
                        resp = requests.head(self.path, stream=True, allow_redirects=True)                        

                except:
                    print ('excepcion en el request: %s %s' % (self.what,self.path))

                    respuesta=self.int_get_html_message('Se ha producido una excepción accediendo a la URL<blockquote>%s</blockquote>' % (self.path))
                    self.int_send_HEADERS(504, respuesta)
                    self.int_send_BODY(respuesta)
                    #self.send_response(504)
                    #self.end_headers()
                else:
                    if DEBUG: print('else')
                    if DEBUG: pprint(vars(resp))

                    # Es un código http valido?
                    if  (resp.status_code == requests.codes.ok):
                            # enviamos el codigo
                        try:
                            self.send_response(resp.status_code)
                            # Procesamos las cabeceras para reescribirlas
                            parsed_headers = Headers(response=resp, debug=False, 
                                                     ip=self.client_address[0],
                                                     port = self.client_address[1])
                            returned_headers = parsed_headers.parsed_headers()

                            # Enviamos todas las cabeceras reescritas
                            for header in returned_headers:
                                self.send_header(header[0], header[1])

                            # Fin de cabeceras

                            self.end_headers()


                            if self.what != 'HEAD':
                                self.wfile.write(resp.content)


                        except: # si encontramos una excepcion...
                            sys.stderr.write("excepcion a")
                            pass 
                        # NO es codigo ok
                        else:
                            pass

            else:
                self.int_HEAD_PROXY_AUTH()
        if DEBUG: print ("end")
        return

    def do_CONNECT(self):
        o_port_default = None
        o_port = 80

        self.parse_query()
        if DEBUG:
            pprint (self.parsed_path)

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
            if DEBUG: print ('Outbound conection to %s:%s' % (o_dest, o_port))
            self.server_socket = socket.create_connection((o_dest, o_port),timeout=3)

        except (socket.error, socket.herror, socket.gaierror) as e:
            if DEBUG: print ("Error %s" % e)
            self.send_response(404,'CONNECT error ['+str(e)+'] to '+o_dest+':'+str(o_port))
            self.end_headers()              

        except socket.timeout as e:
            if DEBUG: print ("Error %s" % e)
            self.send_response(504,'CONNECT Timeout ['+str(e)+'] to '+o_dest+':'+str(o_port))
            #self.send_header('Content-Length', '0')
            self.end_headers()            

        else:      
            self.send_response(200,'CONNECT OK -> '+o_dest+':'+str(o_port))
            self.send_header('Content-Length', '0')
            self.end_headers() 

            self.server_wfile = self.server_socket.makefile('wb', self.wbufsize)            

            self.pdebug('_Csrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)		

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

                #pprint(e)
                if e != [] and not salir_bucle:
                    # cualquiera que sea el error en los sockets de cliente o servidor, tenemos que salir..

                    if self.connection in e:
                        if DEBUG: print ("error socket cliente: cerrandolo")
                    if server_socket in e:
                        if DEBUG:print ("error socket servidor: cerrandolo")
                    if DEBUG: pprint(e)
                    salir_bucle=True

                if r != [] and not salir_bucle:
                    if DEBUG: pprint(r)
                    if (self.connection in r) and not salir_bucle:
                        if DEBUG: print('cliente tiene datos: leyendo cliente')  
                        try:
                            sockdata = self.connection.recv(4096)
                            if (sockdata):
                                self.server_wfile.write(sockdata)
                            else:
                                if DEBUG: print("Cierre de socket cliente ordenado")
                                salir_bucle=True   
                        except (socket.timeout, socket.error) as e:
                            if DEBUG: print("error socket: %s" % (e))
                            salir_bucle=True   

                    if (self.server_socket in r) and not salir_bucle:
                        if DEBUG: print('servidor tiene datos: leyendo servidor')               
                        try:
                            sockdata = self.server_socket.recv(4096)
                            if (sockdata):
                                self.wfile.write(sockdata)
                            else:
                                if DEBUG: print("Cierre de socket servidor ordenado")
                                salir_bucle=True
                        except (socket.timeout, socket.error) as e:
                            if DEBUG: print("error socket: %s" % (e))
                            salir_bucle=True   

                if w != [] and not salir_bucle:
                    if DEBUG: pprint(w)

        if DEBUG: print ("saliendo del bucle del socket...")
        self.server_wfile.close()
        self.server_socket.close()
        return

##     __verbs_supported ='GET, HEAD, POST, PUT, TRACE, OPTIONS, CONNECT'
##                         xxx  xxxx  xxxx              xxxxxxx  xxxxxxx

    def do_OPTIONS(self):
        self.content = ''
        if (self.path == '*'):
            self.send_response(200)
            self.send_header('Allow',self.__verbs_supported)
            self.send_header('Content-Length', '0')	
            self.end_headers            
        else:
            self.BASIC(what='OPTIONS')
            # TODO:: OPTIONS de url requiere auth... gesionado en BASIC      
        self.pdebug('_Osrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)
        return    

    def do_HEAD(self):
        self.content = ''
        self.BASIC(what='HEAD')
        self.pdebug('_Hsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)
        return

    def do_TRACE(self):
        self.content = ''
        self.BASIC(what='TRACE')
        self.pdebug('_Tsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)
        return

    def do_GET(self):
        if 'Content-Length' in self.headers:
            self.content = self.rfile.read(int(self.headers['Content-Length']))
        else:
            self.content = ''        
        self.BASIC(what='GET')
        self.pdebug('_Gsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)
        return


    def do_POST(self):
        if 'Content-Length' in self.headers:
            self.content = self.rfile.read(int(self.headers['Content-Length']))
        else:
            self.content = ''
        pprint(self.content)
        sys.stderr.write('calling BASIC\n')
        self.BASIC(what='POST')
        self.pdebug('_Psrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)
        return


    def do_OTHER(self):
        self.content = ''
        self.send_response(405)
        self.send_header('Allow',self.__verbs_supported)
        self.end_headers
        self.pdebug('_Xsrc: '+self.client_address[0] +',\tPermit: '+str(self.Allowed)+',\tprxUSR: '+self.proxy_user+',\tPRX: '+self.path)
        return