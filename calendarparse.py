#!/usr/bin/python
# -*- coding: utf-8 -*-

from ics import Calendar, Event
import arrow
import postopenhab

def complete_filename(filename):
	return "/opt/openhab/calendar/" + filename

def find_events(day=None, file_or_list=None):
	result_list = []

	# default is today
	d = arrow.utcnow() if (day is None) else arrow.get(day)
			
	files = []
	# can get simple str or complete list
	if isinstance(file_or_list, str):
		files.append(file_or_list)
	else:
		files = file_or_list
		
	for file in files:
		cal = Calendar(open(complete_filename(file)).read().decode("utf-8"))

		# only one event can happen
		if len(cal.events.at(d)) > 0:
			names_list = []
			for evt in cal.events.at(d):
				names_list.append(evt.name)
			result_list.append(', '.join(names_list))
	return result_list
	
def find_events_str(day=None, file_or_list=None):
	events_list = find_events(day=day, file_or_list=file_or_list)
	return ', '.join(events_list)
	
def print_events(day=None, file_or_list=None):
	print(find_events_str(day=day, file_or_list=file_or_list))
	
def post_event_to_openhab(day, itemname, file_or_list):
	text = find_events_str(day=day, file_or_list=file_or_list)

	if (text is not None):
		postopenhab.post_value_to_openhab(itemname, text)
	else:
		postopenhab.post_value_to_openhab(itemname, "")
		
def post_today_event_to_openhab(itemname, file_or_list):
	day = arrow.utcnow()	
	post_event_to_openhab(day, itemname, file_or_list)

def post_tomorrow_event_to_openhab(itemname, file_or_list):
	day = arrow.utcnow()
	day = day.replace(days=+1)
	post_event_to_openhab(day, itemname, file_or_list)

		
