#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2

class EnergeniePowerSwitch(object):
# used to control EG-PM2-LAN from energenie
	
	def __init__(self, hostname, password):
		self.hostname = hostname
		self.password = password
		self.lastresponse = None
		self.loggedin = False
		
	def get_states(self):
		if not self.loggedin:
			raise RuntimeError("You need to login first.")
		data = self._parse_login_response(self.lastresponse)
		result = data
		return result
		
	def get_state(self, port_number):
		if not self.loggedin:
			raise RuntimeError("You need to login first.")
		if port_number > 4 or port_number < 1:
			raise RuntimeError("Wrong port number.")
		val = self.get_states()[port_number-1]
		if "1" == val:
			return True
		else:
			return False

	def set_state(self, port_number, state):
		if not self.loggedin:
			raise RuntimeError("you need to login first.")
		if port_number > 4 or port_number < 1:
			raise RuntimeError("Wrong port number.")
		port = "1" if state else "0"
		url = "http://" + self.hostname
		url_params = "cte" + str(port_number) + "=" + port
		header = {"Content-Type":"text/plain"}
		req = urllib2.Request(url, url_params.encode('utf-8'), header)
		
		response = urllib2.urlopen(req)
		response_read = response.read()
		if not self._is_good_return(response_read):
			raise RuntimeError("Login not successful, check hostname and password.")
		self.lastresponse = response_read
		return True
		
	def login(self):
		if self.loggedin:
			return True
		url = "http://" + self.hostname + "/login.html"
		url_params = "pw=" + self.password
		header = {"Content-Type":"text/plain"}
		req = urllib2.Request(url, url_params.encode('utf-8'), header)
		try:
			response = urllib2.urlopen(req)
			response_read = response.read()
			if not self._is_good_return(response_read):
				raise RuntimeError("Login not successful, check hostname and password.")
			self.lastresponse = response_read
			self.loggedin = True
			return True
		except (urllib2.HTTPError, urllib2.URLError) as e:
			self.loggedin = False
			self.lastresponse = None
			raise e
		
	def logout(self):
		if not self.loggedin:
			return
		url = "http://" + self.hostname + "/login.html"
		url_params = "nothing"
		header = {"Content-Type":"text/plain"}
		req = urllib2.Request(url, url_params.encode('utf-8'), header)
		try:
			response = urllib2.urlopen(req)
			response_read = response.read()
			self.lastresponse = response_read
			self.loggedin = False
		except Exception:
			self.loggedin = False
			self.lastresponse = None
			raise e
	
	def _get_socketstates(self, response):
		return response.rfind("var sockstates =")
	
	def _is_good_return(self, response):
		indx = self._get_socketstates(response)
		if indx > 0:
			return True
		else:
			return False
			
	def _parse_login_response(self, response):
		indx = self._get_socketstates(response)
		sli = response[indx + 18:indx + 25]
		spl = sli.split(",")
		return spl
	