#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import select, time

TRACE = True
MAX_CON_MSG = 180

class Log:
    def get_timestamp(self, timestamp=None):
	    if timestamp is None:
		    timestamp = time.time()
	    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
	    s = "%04d.%2d.%2d %02d:%02d:%02d" % (
	            year, month, day, 
	            hh, mm, ss)
	    return s

    def pdebug(self,message):
	    if TRACE:
		    if len(message) > MAX_CON_MSG:
			    sys.stderr.write('%s - %s\n' % (self.get_timestamp(), message[0:MAX_CON_MSG-3]+'..'))
		    else:
			    sys.stderr.write('%s - %s\n' % (self.get_timestamp(), message))
	    return    
    