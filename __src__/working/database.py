#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import sqlite3 as lite
import sys, os

configdb = "database/config.db"

dir = os.path.dirname(configdb)




try:
    os.stat(dir)
except:
    os.mkdir(dir)
    
