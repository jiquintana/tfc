#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import sqlite3 as lite
import sys, os
import Config
from sqlalchemy import *
from pprint import pprint


class database:
    
    APPID = 0xDECA
    connections={}
    #PRAGMA application_id = APPID
    #PRAGMA encoding = "UTF-8";
    #PRAGMA temp_store=MEMORY;
    #PRAGMA journal_mode=MEMORY;
    #PRAGMA auto_vacuum = FULL;
    
    def __init__(self):    
        for dbname in Config.dbFiles.keys():
            filename = Config.dbFiles[dbname]
            pathname = os.path.dirname(filename)
            
            sys.stdout.write('Checking if database "'+dbname+'" stored in '+filename+' exists\n')
            
            try:
                os.stat(pathname)
            except:
                sys.stdout.write('Directory of '+filename+' doesn\'t exists. Trying to create ['+pathname+']...\n')
                os.mkdir(pathname)
            
            self.connections[dbname] = lite.connect(filename)
        return
    
    
    ROL = {
        'Administrador': 0,
        'Usuario privilegiado': 1,
        'Usuario': 2,
        'Invitado': 3
    }
    
    class proxyUser:
        name=''
        rol=''
        user=''
        password=''
        
        def __init__(name, rol, user, password):
            self.name = name
            self.rol = rol
            self.user = user
            self.password = password

        
    

mydatabases = database()

logdb = mydatabases.connections['log']

with logdb:
    cur=logdb.cursor()
    cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
    cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
    cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
    cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
    cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
    cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
    cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
    cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
    cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")    



'''
try:
    os.stat(dir)
except:
    os.mkdir(dir)
'''    
