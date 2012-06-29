"""
Checks specified Github private feed every 5 mins
and notifies via Growl if there's any new activity.

by Aditya Mukherjee 
"""
# TODO different titles for different activity type

import sys
import thread
import requests
import feedparser
import gntp.notifier
from urlparse import urlparse
from time import sleep

last_id = None

growl = gntp.notifier.GrowlNotifier(
    applicationName = "Github Notifier",
    notifications = ["New Activity"],
    defaultNotifications = ["New Activity"],
)
growl.register()

def notify(title, icon, callback):
	"""
	Outsource the actual notification to this function
	so that I can take my own time fetching the icon.
	"""

	url = urlparse(icon)
	params = dict([part.split('=') for part in url.query.split('&')])

	# break down the url and reconstruct a proper one
	icon_url = "%s://%s%s" % (url.scheme, url.netloc, url.path)
	icon_url = "%s?s=60&d=%s" % (icon_url, params['d'])

	r = requests.get(icon_url).content

	growl.notify(
		noteType = "New Activity",
		title = "Github",
		description = title,
		icon = r, # binary data because URL support was removed in 1.3.3 (http://j.mp/JZ00Vu)
		sticky = False,
		callback = callback,
	)

def get_latest():
	"""
	Fetches the feed and passes appropriate data
	to `notify` in a new thread.
	"""

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
				thread.start_new_thread(notify, (i.title, i.media_thumbnail[0]['url'], i.link))
		last_id = feed.entries[0].id # this is the latest notification sent
		sleep(300)

get_latest()
