#!/usr/bin/python
# -*- coding: utf-8 -*-

# pip install feedparser

import feedparser
import phoneIntegration

hit_list = ["http://www.spiegel.de/schlagzeilen/index.rss", "http://www.stuttgarter-zeitung.de/rss/topthemen.rss.feed"]
feeds = [feedparser.parse(rss_url) for rss_url in hit_list]

text_to_speak = ""
for feed in feeds:
	for item in feed["items"]:
		text_to_speak += item["title"] + " . . . "
	
#print(text_to_speak)
	
phoneIntegration.speak(text_to_speak)
