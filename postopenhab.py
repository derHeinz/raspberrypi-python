#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import xml.etree.ElementTree as ET

def post_systemnotification(message, type):
	post_value_to_openhab("SystemNotification", (type + '#' + message))
	
def post_value_to_openhab(itemname, value):
	# construct URL
	url = 'http://localhost:8080/rest/items/' + itemname
	# need to have this header all other headers are ignored!
	header = {"Content-Type":"text/plain"}
	params_bytes = value.encode('utf-8')
	req = urllib2.Request(url, params_bytes, header)
	response = urllib2.urlopen(req)
		
def get_switch_value_from_openhab(itemname):
	url = 'http://localhost:8080/rest/items/' + itemname
	# need to have this header all other headers are ignored!
	header = {"Content-Type":"text/plain"}
	req = urllib2.Request(url, None, header)
	res = urllib2.urlopen(req)
	root = ET.fromstring(res.read())
	val = root.findall(".//state")[0].text
	if ("OFF" == val):
		return False
	elif ("ON" == val):
		return True
	else:
		return None
	
	return urllib2.urlopen(req)