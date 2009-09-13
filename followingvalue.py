"""
+1 if one hashtag in tweet, -0.5 for every hashtag after the first one // categorisation, easier discoverability of tweet
+1 for any mentions // promoting and helping discover new users
+1 for every link // promoting content, new stuff
+1 if a retweet // proper attribution
"""

import simplejson, base64, urllib, urllib2, re, time, threading, sys

try:
	if sys.argv[1] == '--help':
		print """Calculate the value of the people you're following
by running some basic rule-based analysis of their
last 200 tweets.

Requires: simplejson"""
		exit()
	else:
		u = sys.argv[1]
		p = sys.argv[2]
except:
	print "Usage: python followingvalue.py <username> <password>\nType 'python followingvalue.py --help' for additional information."
	exit()

def getHashtagValue(t):
	v = 0
	m = re.findall('^#([\w]+)|[ ]#([\w]+)', t)
	c = len(m)
	if c>0 :
		if c>1 :
			v = 1-(c-1)*0.5
		else:
			v = 1
	else:
		v = 0
	return v

def getMentionValue(t):
	c = re.findall('@([\w]+)', t)
	return len(c)

def getLinksValue(t):
	c = re.findall('(http://(?:\S)+)', t)
	return len(c)

def getRetweetValue(t):
	c = len(re.findall('RT|via', t))
	if c>0 :
		return 1
	else:
		return 0

def getValue(userid):
	# print("Doing " + str(userid))
	value = 0
	
	url = 'http://twitter.com/statuses/user_timeline/'+ str(userid) +'.json?count=200'
	headers = {'Authorization': 'Basic ' + base64.b64encode(u+':'+p)}
	
	req = urllib2.Request(url, headers=headers)
	try:
		response = urllib2.urlopen(req)
	except:
		print "-"*10 + "\nFailed for " + str(userid) + ". Twitter must be stressed, continuing after 5 seconds ...\n" + "-"*10
		time.sleep(5)
		getValue(userid)
		return

	json = simplejson.loads(response.read())
	
	for i in json:
		text = i['text']
		value += getHashtagValue(text)
		if i['in_reply_to_screen_name'] != "":
			value += 0
			# r = 0
		else:
			value += getMentionValue(text)
			# r = getMentionValue(text)
		
		value += getLinksValue(text)
		value += getRetweetValue(text)
		# values = [getHashtagValue(text), r, getLinksValue(text), getRetweetValue(text)]
	
	username = json[0]['user']['screen_name']
	print username + ' / ' + str(value)

""" multithreaded love """
class GenerateValue (threading.Thread):
	def __init__(self, userid):
		threading.Thread.__init__(self)
		self.userid = userid
	
	def run(self):
		getValue(self.userid)

url = 'http://twitter.com/friends/ids/'+ u +'.json'
headers = {'Authorization': 'Basic ' + base64.b64encode(u+':'+p)}

req = urllib2.Request(url, headers=headers)
try:
	response = urllib2.urlopen(req)
except Exception:
	print errno

for i in simplejson.loads(response.read()):
	thread = GenerateValue(i)
	thread.start()