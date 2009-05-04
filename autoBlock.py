# do a Twitter search for 'to:spam', and block and handles mentioned in the tweet

import urllib, urllib2, simplejson, re, base64

# make call to Twitter Search

url = 'http://search.twitter.com/search.json?q=to:spam&page=2'
user = '' # your username
pswd = '' # your password

r = urllib2.urlopen(url)
json = simplejson.load(r)['results']

for i in json:
	p = re.compile('@([a-zA-Z0-9\-_\.+:=]+\w)')
	users = p.findall(i['text'])
	for j in users:
		handle = j.replace('@', '');
		if handle == 'spam':
			pass
		else:
			try:
				req = urllib2.Request('http://twitter.com/blocks/create/'+ handle +'.json', {}, {'Authorization': 'Basic ' + base64.b64encode(user + ':' + pswd)})
				res = urllib2.urlopen(req)
			except:
				print 'couldn\'t block "'+ handle +'"'
			else:
				r = simplejson.load(res)
				print '"'+ r['name'] +'" blocked'
				