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



	def do_GET(self):
		
		parsed_headers = Headers(headers=self.headers.items(), debug=True, 
		                        ip=self.client_address[0],
		                        port = self.client_address[1])
		returned_headers = parsed_headers.input_parsed_headers()
		
		self.send_response(200)
		self.end_headers()
		return

