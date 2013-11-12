#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number:syntax=on:set filetype indent plugin on

MAX_LEN_MSG = 140
NUM_THREADS = 180

config_Path = "./db"
cache_Path = "./cache"
log_Path = "./cache"

dbFiles = {
    'config': config_Path+'/config.db',
    'rules': config_Path+'/rules.db',
    'log': config_Path+'/log.db'
}

