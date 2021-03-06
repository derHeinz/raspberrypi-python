#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
import json

class RaspberryHealth:

    def __init__(self, ip_or_dns):
        self._address = "http://" + ip_or_dns + ":5005" + "/v1.0/query/"
    
    def _get(self, name):
        url = self._address + name    
        header = {"Content-Type":"application/json"}
        req = Request(url, None, header)
        response = urlopen(req)
        return json.load(response)[name]
        
    def get_cpu_temp(self):
        return self._get("cpu_temp")

    def get_cpu_clock(self):
        return self._get("cpu_clock")
        
    def get_sys_temp(self):
        return self._get("sys_temp")
        
    def get_external_temp(self):
        return self._get("external_temp")
        
    def get_external_hum(self):
        return self._get("external_hum")
