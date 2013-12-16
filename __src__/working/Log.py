#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import select, time, sys, datetime
from Config import Config
import traceback


TRACE = True


class Log:

    def get_timestamp(self):
        return str(datetime.datetime.now())


    def pdebug(self,*args):
        if TRACE:
            try:
                if (args[0].__len__()) > Config.MAX_LEN_MSG:
                    sys.stdout.write('%s, %s\n' % (self.get_timestamp(), args[0][0:Config.MAX_LEN_MSG-3]+'..'))
                else:
                    sys.stdout.write('%s, %s\n' % (self.get_timestamp(), args[0]))
            except Exception as e:
                print(traceback.format_exc())
                print(args)
                print('!!! Log exception %s, %r' % (e, len(args)))
        return
