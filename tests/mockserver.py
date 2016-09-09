# Copyright 2016 Eyevinn Technology. All rights reserved
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.
# Author: Jonas Birme (Eyevinn Technology)
from os.path import dirname, abspath, join
from bottle import route, run, response, redirect
import bottle
import time

mockups = abspath(join(dirname(__file__), 'mockups'))

@route('/validlive/master.m3u8')
def validlivemaster():
    response.set_header('Content-Type', 'application/vnd.apple.mpegurl')
    return mockup_file('validlive-master.m3u8')    

@route('/validlive/master2500.m3u8')
def validlivemedia2500():
    response.set_header('Content-Type', 'application/vnd.apple.mpegurl')
    return mockup_file('validlive-master2500.m3u8')    

@route('/validlive/master1500.m3u8')
def validlivemedia1500():
    response.set_header('Content-Type', 'application/vnd.apple.mpegurl')
    return mockup_file('validlive-master1500.m3u8')    

@route('/vod/master.m3u8')
def validvodmaster():
    response.set_header('Content-Type', 'application/vnd.apple.mpegurl')
    return mockup_file('validvod-master.m3u8')    

@route('/vod/master2500.m3u8')
def validvodmedia2500():
    response.set_header('Content-Type', 'application/vnd.apple.mpegurl')
    return mockup_file('validvod-master2500.m3u8')    


def mockup_file(filename):
    with open(join(mockups, filename)) as fileobj:
        return fileobj.read().strip()

run(host='localhost', port=8111)
