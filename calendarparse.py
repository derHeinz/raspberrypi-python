#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ics import Calendar, Event
from ics.timeline import Timeline
import arrow
from . postopenhab import post_value_to_openhab

def complete_filename(filename):
    return "/etc/openhab2/calendar/" + filename

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
        cal = Calendar(open(complete_filename(file)).read())
        tl = Timeline(cal)

        # only one event can happen
        names_list = []
        for evt in tl.at(d):
            names_list.append(evt.name)
        
        if names_list:
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
        post_value_to_openhab(itemname, text)
    else:
        post_value_to_openhab(itemname, "")
        
def post_today_event_to_openhab(itemname, file_or_list):
    day = arrow.utcnow()    
    post_event_to_openhab(day, itemname, file_or_list)

def post_tomorrow_event_to_openhab(itemname, file_or_list):
    day = arrow.utcnow()
    day = day.replace(days=+1)
    post_event_to_openhab(day, itemname, file_or_list)
