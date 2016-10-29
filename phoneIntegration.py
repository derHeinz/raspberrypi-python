#!/usr/bin/python
# -*- coding: utf-8 -*-

#import urllib.request as urllib2 # change this potentially on raspi
import urllib2
import json
import base64
import os

def currentAddress():
	return "http://" + "address" + ":5000"

def get_brightness(base_url=currentAddress()):
	# construct url
	url = base_url + "/getBrightness"
	print(url)
	# prepare request
	header = {}
	req = urllib2.Request(url, None, header)
	print(req)
	response = urllib2.urlopen(req)
	bright_res_json = json.load(response)
	return bright_res_json['light']
	
def speak(value, base_url=currentAddress()):
	# construct url
	url = base_url + "/speak"
	# prepare request
	header = {"Content-Type":"text/plain; charset=utf-8"}
	# consider value given as utf-8 as this is default for our python scripts
	value = base64.b64encode(value.encode("utf-8"))
	params_bytes = value.encode('utf-8')
	req = urllib2.Request(url, params_bytes, header)
	response = urllib2.urlopen(req)
	
def uploadFile(filepath, base_url=currentAddress()):
	filename = os.path.basename(filepath)
	#read the file in base64
	encoded_string = ""
	with open(filepath, "rb") as file:
		encoded_string = base64.b64encode(file.read())
		
	# create request
	url = base_url + "/storeFile/" + filename
	header = {"Content-Type":"application/json"}
	#value = bytes('{ file=\"', 'utf-8') + encoded_string + bytes('\" }', 'utf-8')
	value = '{ file=\"' + encoded_string + '\" }'
	req = urllib2.Request(url, value, header)
	response = urllib2.urlopen(req)
	

def playFile(filepath, base_url=currentAddress()):
	filename = os.path.basename(filepath)
	url = base_url + "/playAudio/" + filename
	header = {"Content-Type":"text/plain"}
	
	# create request
	req = urllib2.Request(url, bytearray([" "]), header)
	try:
		response = urllib2.urlopen(req)
		return True
	except urllib2.HTTPError as e:
		if (e.code == 404):
			return False
		raise e
	
def playFileWithPotentialUpload(filepath, base_url=currentAddress()):
	if (not playFile(filepath, base_url)):
		print("uploading")
		uploadFile(filepath, base_url)
		playFile(filepath, base_url)
		
	