#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ics import Calendar, Event
from ics.timeline import Timeline
import arrow

def _complete_filename(filename):
    return "/etc/openhab2/calendar/" + filename

def _find_events(day=None, file_or_list=None):
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
        cal = Calendar(open(_complete_filename(file)).read())
        tl = Timeline(cal)

        # only one event can happen
        names_list = []
        for evt in tl.at(d):
            names_list.append(evt.name)
        
        if names_list:
            result_list.append(', '.join(names_list))

    return result_list
    
def _find_events_str(day, file_or_list):
    events_list = _find_events(day=day, file_or_list=file_or_list)
    return ', '.join(events_list)
    
def get_event_str(dayshift, file_or_list):
    day = arrow.utcnow()
    day = day.shift(days=dayshift)
    return _find_events_str(day, file_or_list)
    