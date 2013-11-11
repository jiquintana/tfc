#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import select, time, sys, datetime
import Config

TRACE = True
MAX_CON_MSG = 180

class Log:
    def get_timestamp(self):
        return str(datetime.datetime.now())
   

    def pdebug(self,*args):
        if TRACE:
            if (args[0].__len__()) > MAX_CON_MSG:
                sys.stdout.write('%s, %s\n' % (self.get_timestamp(), args[0][0:MAX_CON_MSG-3]+'..'))
            else:
                sys.stdout.write('%s, %s\n' % (self.get_timestamp(), args[0]))
        return    
