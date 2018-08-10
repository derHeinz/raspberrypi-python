#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import re
import os

def find_ips(mac_or_name):
	res = subprocess.check_output(["arp", "-a"])
	lines = res.split(b'\n')
	ips = []

	for line in lines:
		if (mac_or_name in line):
			bla = line.split("(", 1)
			bla = bla[1].rsplit(")", 1)
			ip = bla[0]
			ips.append(ip)
	return ips
	
def check_online(ip):
	if subprocess.call(["ping", "-c1", "-w1", "-t1", ip], stdout=open(os.devnull, 'w')) == 0:
		return True
	return False
				