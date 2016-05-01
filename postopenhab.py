#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2

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