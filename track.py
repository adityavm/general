#!/usr/bin
import sys, urllib2, simplejson, time
from urllib import urlencode
since = 1

while(1):
	json = 0
	result = 0
	
	url = "http://search.twitter.com/search.json?" + urlencode({'q': " ".join(sys.argv[1:len(sys.argv)]), "since_id": str(since)})
	result = urllib2.urlopen(url)

	json = simplejson.load(result)['results']
	json.reverse()

	for i in json:
		print "- " + i['text'].encode('utf-8') + " (" + i['from_user'].encode('utf-8') + ")"

	if len(json) >= 1:
		since = json[len(json)-1]['id']
		print "_"*10
	
	time.sleep(60)