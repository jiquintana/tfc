#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number



global class myglobal():
    
    keep_running = True
    
    def check_keep_running():
        return keep_running
    
    def shutdown():
        keep_running = False 
    