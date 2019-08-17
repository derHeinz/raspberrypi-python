#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os

def find_online_ip(mac_name_ip):
    if (_validate_ip(mac_name_ip)):
        # it's a valid ip - so just return
        return mac_name_ip
    if (_validate_mac(mac_name_ip)):
        # it's a valid mac
        mac = _uniform_mac(mac_name_ip)
        for ip in _find_ips_by_mac(mac):
            if _check_online(ip):
                return ip
       # throw error otherwise
    
    # it must be a name
    name = mac_name_ip
    for ip in _find_ips_by_name(name):
        if _check_online(ip):
            return ip

def find_online_ip_by_mac(mac):
   mac = _uniform_mac(mac)
    
   for ip in _find_ips_by_mac(mac):
       if _check_online(ip):
           return ip

def _validate_mac(potential_mac):
    mac = _uniform_mac(potential_mac)
    parts = mac.split(":")
    # check length of 6
    if len(parts) != 6:
        return False
    # check each part to be alphanumerical hex
    for part in parts:
        try:
            int(part, 16)
        except ValueError:
            return False
    return True
    
def _validate_ip(potential_ip):
    parts = potential_ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        i = int(part)
        if i < 0 or i > 255:
            return False
    return True
    
def _uniform_mac(mac):
    if ("-" in mac):
        mac = mac.replace("-", ":")
    mac = mac.lower()
    return mac
    
def _find_ips_by_mac(mac):
    return _find_ips(mac, False)
    
def _find_ips_by_name(name):
    return _find_ips(name, True)

def _find_ips(mac_or_name, with_names):
    arp_params = "-a"
    if (not with_names):
        # do not show host names
        arp_params += "n"
    res = subprocess.check_output(["arp", arp_params]).decode("utf-8")
    lines = res.split('\n')
    ips = []

    for line in lines:
        if (mac_or_name in line):
            bla = line.split("(", 1)
            bla = bla[1].rsplit(")", 1)
            ip = bla[0]
            ips.append(ip)
            
    return ips

def _check_online(ip):
    if subprocess.call(["ping", "-c1", "-w1", "-t1", ip], stdout=open(os.devnull, 'w')) == 0:
        return True
    return False
                