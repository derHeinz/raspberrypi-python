#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, build_opener, HTTPHandler, Request
import json
import datetime

def post_value_to_openhab(itemname, value):
    # construct URL
    url = _get_baseurl() + itemname
    # need to have this header all other headers are ignored!
    header = {"Content-Type":"text/plain"}
    params_bytes = _params_from_value(value)
    req = Request(url, params_bytes, header)
    response = urlopen(req)
    
def put_value_to_openhab(itemname, value):
    # construct URL
    url = _get_baseurl() + itemname + '/state'
    # need to have this header all other headers are ignored!
    header = {"Content-Type":"text/plain"}
    params_bytes = _params_from_value(value)
    req = Request(url, params_bytes, header)
    req.get_method = lambda: 'PUT'
    opener = build_opener(HTTPHandler)
    response = opener.open(req).read()
    
def get_value_from_openhab(itemname):
    url = _get_baseurl() + itemname
    # need to have this header all other headers are ignored!
    header = {"Content-Type":"text/plain"}
    req = Request(url, None, header)
    result = urlopen(req).read()
    result = result.decode('UTF-8')
    root = json.loads(result)
    val = root['state']

    return val

def get_switch_value_from_openhab(itemname):
    val = get_value_from_openhab(itemname)
    if ("OFF" == val):
        return False
    elif ("ON" == val):
        return True
    else:
        return None
    
    return urlopen(req)
    
def post_now_to_openhab(itemname):
    post_value_to_openhab(itemname, datetime.datetime.now())

def post_systemnotification(message, type):
    post_value_to_openhab("SystemNotification", (type + '#' + message))

def _params_from_value(value):
    if isinstance(value, datetime.datetime):
        time_string = value.strftime("%Y-%m-%dT%H:%M:%S")
        return time_string.encode('utf-8')
    else:
        return value.encode('utf-8')
    
def _get_baseurl():
    return 'http://localhost:8080/rest/items/'
