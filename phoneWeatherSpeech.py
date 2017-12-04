#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib import urlopen
import urllib2
import phoneIntegration

def get_weather_forecast_text():
	url = "http://www.wetter.net/188/Stuttgart"    
	html = urlopen(url).read().decode('iso-8859-1')
	#encoding=req.headers['content-type'].split('charset=')[-1]

	head_list = ["Das Wetter in Stuttgart", "<br><br>", "<br>"]
	tail = "<br><br>"
	forecast_begin_index = 0

	for s in head_list:
		forecast_begin_index = html.find(s, forecast_begin_index)
		forecast_begin_index = forecast_begin_index + len(s)

	forecast_end_index = html.find(tail, forecast_begin_index)

	html_extract = html[forecast_begin_index:forecast_end_index]
	return html_extract


message = get_weather_forecast_text()

try:
	phoneIntegration.speak(message)
except urllib2.URLError:
	postopenhab.post_systemnotification("Speak", "Failed to speak.")

