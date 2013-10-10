#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:sts=4:ai:et:fileencoding=utf-8:number:syntax=on:set filetype indent plugin on

configPath = "./database"

dbFiles = dict(
    name('config'): path(configPath+'/config.db'),
    name('rules'): path(configPath+'/rules.db'),
    name('log'): path(configPath+'/log.db')
)
