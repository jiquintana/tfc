#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import sqlite3 as lite
import sys, os
from config import dbFiles

class database:
    
    def __init__(self):
        for database in dbFiles:
            print database.items()
        return
    
    

mydatabase = database()


'''
try:
    os.stat(dir)
except:
    os.mkdir(dir)
'''    
