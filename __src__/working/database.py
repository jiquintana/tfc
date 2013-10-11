#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number

import sqlite3 as lite
import sys, os
from config import dbFiles


'''
class database:
    
    APPID = 0xDECA
    #PRAGMA application_id = APPID
    #PRAGMA encoding = "UTF-8";
    #PRAGMA temp_store=MEMORY;
    #PRAGMA journal_mode=MEMORY;
    #PRAGMA auto_vacuum = FULL;
    
    def __init__(self):
        
        for dbname in dbFiles.keys():
            filename = dbFiles[dbname]
            pathname = os.path.dirname(filename)
            
            print 'Checking '+dbname+':\t'+filename
            
            try:
                os.stat(pathname)
            except:
                print 'Path of '+filename+' doesn\'t exists. Trying to create..'
                os.mkdir(pathname)
            
            
        return
    
    
    ROL = {
        'Administrador': 0,
        'Usuario privilegiado': 1,
        'Usuario': 2,
        'Invitado': 3
    }
    
    class proxyUser:
        name,
        rol,
        user,
        password
        
        def __init__(name, rol, user, password):
            self.name = name
            self.rol = rol
            self.user = user
            self.password = password
        
        def 
        
    

mydatabase = database()

'''
'''
try:
    os.stat(dir)
except:
    os.mkdir(dir)
'''    
