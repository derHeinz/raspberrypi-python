#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
import json

class RadioAlarmClock:

    def __init__(self, ip_or_dns):
        self._address = "http://" + ip_or_dns + ":5000" + "/v1.0/"
    
    def _get(self, name):
        url = self._address + name    
        header = {"Content-Type":"application/json"}
        req = Request(url, None, header)
        response = urlopen(req)
        return json.load(response)[name]
        
    def _set(self, name, value):
        url = self._address + name
        header = {"Content-Type":"application/json"}
        value_as_bytes = bytes(value, "UTF-8")
        req = Request(url, value_as_bytes, header)
        response = urlopen(req)
        return json.load(response)["result"]

    def get_alarmtime(self):
        return self._get("alarmtime_1")

    def set_alarmtime(self, time):
        str = "alarmtime_1"
        value = json.dumps({str: time})
        return self._set(str, value)

    def get_alarm(self):
        return self._get("alarm_1")

    def set_alarm(self, onoff):
        str = "alarm_1"
        value = json.dumps({str: onoff})
        return self._set(str, value)
        
    def get_play(self):
        return self._get("play")
        
    def set_play(self, onoff):
        str = "play"
        value = json.dumps({str: onoff})
        return self._set(str, value)
