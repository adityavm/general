"""
Checks specified Github private feed every 5 mins
and notifies via Growl if there's any new activity.

by Aditya Mukherjee 
"""
# TODO different titles for different activity type

import sys
from time import sleep
import feedparser
import gntp.notifier
from pprint import pprint

last_id = None

growl = gntp.notifier.GrowlNotifier(
    applicationName = "Github Notifier",
    notifications = ["New Activity"],
    defaultNotifications = ["New Activity"],
)
growl.register()

def get_latest():
	global last_id

	while(1):
		# get feed
		feed = feedparser.parse(sys.argv[1])

		for i in feed.entries[0:10]: # limit to 10
			# if this entry's id matches the last notification id, stop
			if i.id == last_id:
				break
			else:
				# notify
				growl.notify(
					noteType = "New Activity",
					title = "Github Activity",
					description = i.title,
					icon = i.media_thumbnail[0]['url'],
					sticky = False,
					callback = i.link,
				)
		last_id = feed.entries[0].id # this is the latest notification sent
		sleep(300)

get_latest()
