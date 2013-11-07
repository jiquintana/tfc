#!/usr/bin/python
# -*- coding: utf-8 -*-
# header_valueim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

class Headers:


	DEBUG = False
	via_header_seen = False
	headers_have_been_parsed = False
	__original_headers = []
	__headers = []
	doclen = 0
	ip = ''
	port = ''     

	def __init__(self,  headers=None, cookies=None, doclen=0, debug =False,
	             ip='', port='', server_version='HTTP_Proxy/0.1'):
		self.doclen=doclen
		self.__original_headers = []
		self.__headers = []
		self.ip = ''
		self.port = ''        
		if debug in [True, False]:
			self.DEBUG=debug
		if self.DEBUG: print ('Headers.__init__')        
		if headers != None:
			self.__original_headers = headers.copy()
		if cookies != None:
			self.__original_cookies = cookies.copy()			

		self.DEBUG = debug
		self.ip = ip
		self.port = port
		self.server_version = server_version

	def output_parsed_headers(self):
		if self.DEBUG: print ('Headers.output_parsed_headers')
		if not self.headers_have_been_parsed:
			self.output_parse()   
		return self.__headers

	def input_parsed_headers(self):
		if self.DEBUG: print ('Headers.input_parsed_headers')
		
		if not self.headers_have_been_parsed:
			self.input_parse()   
		return self.__headers

	def dump(self):
		if self.DEBUG: print ('Headers.dump')

		for i in self.__headers.headers:
			print (' > %s %s: %s' % (self.port, i, self.__headers[i])) 
		if self.headers_have_been_parsed:
			for i in self.__headers:
				print (' < %s %s:' % (self.port, i))

	def output_parse(self):
		if self.DEBUG: print ('Headers.output_parse')     
		for header_name, header_value in self.__original_headers.items():
			if self.DEBUG: print('IN header: %s - %s: %s' % (self.port,header_name.capitalize(),header_value))
			if (header_name == 'date'):
				pass
			elif (header_name== 'content-length'):
				# Debido a que la librería request hace descompresion automatica, no nos podemos
				# fiar del header 'content-length' en caso de codificacion deflate/gzip, asi que
				# reescribimos la cabecera incondicionalmente

				self.__headers.append([header_name.capitalize(), self.doclen])
				if self.DEBUG:
					print('OU header CL: %s - %s: %s' % (self.port,header_name.capitalize(),header_value))
					print('OU header SZ: %s -   : %s' % (self.port, self.doclen))
				pass
			elif (header_name == 'transfer-encoding'):
				# Eliminamos transfer-encoding por la misma razon anterior 
				if self.DEBUG: print('SU header: %s - %s: %s' % (self.port,header_name.capitalize(),header_value))

			elif (header_name=='content-encoding'):
				# Eliminamos transfer-encoding por la misma razon anterior
				if self.DEBUG: print('SU header: %s - %s: %s' % (self.port,header_name.capitalize(),header_value))
			elif (header_name== 'via'):
				self.via_header_seen = True
				# Agnadimos la cabecera via
				header_value+=', http/1.0 '+self.server_version
				self.__headers.append([header_name.capitalize(),header_value])
				if self.DEBUG: print('OU header: %s - %s: %s' % (self.port,header_name.capitalize(),header_value))                            

			elif (header_name == 'server'):
				# la escribe directamente el servidor BaseHTTPServer
				if self.DEBUG: print('SU header: %s - %s: %s' % (self.port,header_name.capitalize(),header_value))

			elif (header_name == 'set-cookie'):
				from requests.cookies import get_cookie_header		    
				# Este bloque gestiona las cookies; Requests devuelve todas las cookies en un array 'set-cookie', pero indistinguible si hay varias.
				# para obtener todos los parámetros y reenviarlos, parseamos la cadena.		
				def allindices(string, sub, listindex=[], offset=0):
					i = string.find(sub, offset)
					while i >= 0:
						listindex.append(i)
						i = string.find(sub, i + 1)
					return listindex				    

				# inicializamos el vector POS con valor 0 y longitud de la cadena
				POS = [0,len(header_value)]

				# Para cada una de las cookies encontradas en los headers...
				for cookie in self.__original_headers.cookies.keys():
					# buscamos la cookie en formato ", cookie=" y agnadimos todas las posiciones al vector POS
					for i in allindices(header_value, ', '+cookie+'='): POS.append(i)
					# buscamos la cookie en formato "cookie=" y agnadimos todas las posiciones al vector POS
					for i in allindices(header_value, cookie+'='): POS.append(i)


				#for header_nameey in resp.cooheader_nameies.header_nameeys():
				#   for i in allindices(header_value, ', '+header_nameey+'='): POS.append(i)
				#  for i in allindices(header_value, header_nameey+'='): POS.append(i)

				# Eliminamos los valores duplicados en el array POS
				POS=list(set(POS))
				# y lo ordenamos
				POS.sort()

				# ahora tenemos un array con las posiciones de las cookies a cortar					
				while (POS != []):
					parsed_cookie=header_value[POS[0]:POS[1]]
					#self.send_header('Set-Cookie',parsed_cookie)
					self.__headers.append(['Set-Cookie',parsed_cookie])
					if self.DEBUG: 
						print ("\t... cookie: Set-cookie=%s" % (header_value[POS[0]:POS[1]]))                    

					# eliminamos las posiciones 0 y 1; como eliminamos primero el valor [0], el valor [1]
					# se convierte en la segunda llamada en [0]
					POS.remove(POS[0])
					POS.remove(POS[0])
				pass



			else:
				if self.DEBUG: print('OU header: %s - %s: %s' % (self.port,header_name.capitalize(),header_value)) 
				self.__headers.append([header_name.capitalize(),header_value])

				#self.send_header(header_name.capitalize(),header_value)
				#print(resp.content)

		if (not self.via_header_seen):
			# Agnadimos a cabecera via
			header_name='Via'
			header_value='http/1.0 '+self.server_version
			self.__headers.append([header_name.capitalize(),header_value])   
			if self.DEBUG: print('OU header: %s - %s: %s' % (self.port,header_name,header_value))                            

		self.headers_have_been_parsed = True

		return


	def input_parse(self):
		if self.DEBUG: print ('Headers.input_parse')     
		for header_name, header_value in self.__original_headers:
			if self.DEBUG: print('IN header: %s - %s: %s' % (self.port,header_name.capitalize(),header_value))
			
		return


	def headers():
		return self.__headers