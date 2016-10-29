#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from ics import Calendar, Event
from urllib2 import urlopen # import requests

# create url for the current year in germany BW.
#url = "http://www.kayaposoft.com/enrico/ics/v1.0?country=deu&fromDate=01-01-" + str(datetime.today().year) + "&toDate=31-12-" + str(datetime.today().year) + "&region=Baden-W%C3%BCrttemberg"
# decode from that url
#c = Calendar(urlopen(url).read().decode('utf-8'))
c = Calendar(open("/home/pi/Terminkalender.ics").readlines())


# append special date - just for tests:
#begin_dt = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
#e = Event(name="Heuer", begin = begin_dt, duration=timedelta(days=1))
#c.events.append(e)

print c.events

# check whether there is one matching event:
if len(c.events.now()) > 0:
	#c.events.now[0]
	print c.events.now()[0].name
else:
	print ""