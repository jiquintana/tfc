#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import select, time, sys
import Config

TRACE = True
MAX_CON_MSG = 180

class Log:
    def get_timestamp(timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
        s = "%04d.%02d.%02d %02d:%02d:%02d" % (
            year, month, day, 
            hh, mm, ss)
        return s

    def pdebug(*args):
        if TRACE:
            if len(args[0]) > MAX_CON_MSG:
                sys.stderr.write('%s, %s\n' % (Log.get_timestamp(), args[0][0:MAX_CON_MSG-3]+'..'))
            else:
                sys.stderr.write('%s, %s\n' % (Log.get_timestamp(), args[0]))
        return    
