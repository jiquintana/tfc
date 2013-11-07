#!/usr/bin/python
# -*- coding: utf-8 -*-
# header_valueim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number
import hashlib
import Config
import Log

import os
from pprint import pprint

class FileCache:
	path = ''
	md5hash_str = ''
	cache_filename_base = ''
	cache_filename_meta = ''
	cache_filename_cache = ''
	is_initialized = False
	DEBUG = False

	def __init__(self):
		if not os.path.exists(Config.cachePath):
			os.makedirs(Config.cachePath)
		self.was_checked = False
		self.DEBUG = False

	def setup(self, path, debug=False, ip='', port=''):
		self.path=path
		md5hash = hashlib.md5()
		md5hash.update(bytes(self.path,encoding='utf_8'))
		self.md5hash = md5hash.hexdigest()

		self.cache_filename_base = Config.cachePath + '/' + self.md5hash.upper()
		self.cache_filename_meta = self.cache_filename_base + '.meta'
		self.cache_filename_cache = self.cache_filename_base + '.cache'
		self.is_initialized = True

		if debug == True or self.DEBUG == True:
			Log.pdebug('Filecache.setup dump:')
			Log.pdebug(vars(self))

		return

	def is_cached(self, path, debug=False, ip='', port=''):
		returncode = False
		meta_file_path = ''

		if not self.is_initialized:
			self.setup(path=path)

		if os.path.exists(self.cache_filename_cache):
			try:
				with open(self.cache_filename_meta, 'r') as meta_file:
					meta_file_path = meta_file.read()
			except:
				pass
		if ( meta_file_path == path):
			returncode = True  
		return returncode


	def put(self, path, content, debug=False, ip='', port=''):
		succeded = False

		if not self.is_initialized:
			self.setup(path=path)         

		#self.setup(path)
		#self.cache_filename_base = Config.cachePath + '/' + self.md5hash
		#self.cache_filename_meta = self.cache_filename_base + '.meta'
		#self.cache_filename_cache = self.cache_filename_base + '.cache'       

		try:
			with open(self.cache_filename_meta, 'wb') as meta_file:
				meta_file.write(bytes(path,encoding='utf_8'))

			with open(self.cache_filename_cache, 'wb') as cache_file:
				cache_file.write(content)
			succeded = True  
			if debug == True:
				Log.pdebug('%s:%s, ::: CCH filename: %s' % (ip, port, self.cache_filename_base))
				Log.pdebug('%s:%s, ::: CCH path: %s' % (ip, port, path))
				Log.pdebug('%s:%s, ::: CCH size %s' % (ip, port, len(content)))

		except:
			pass

		return succeded


	def get(self, path):
		succeded = False

		if not self.is_initialized:
			self.setup(path=path)         

		try:    
			with open(self.cache_filename_cache, 'rb') as cache_file:
				content=cache_file.read()
			succeded = True         
		except:
			pass

		return content






