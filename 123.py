import time, urllib2, urllib, base64

while(1):
	t = time.time()
	if t >= 1234567890:
		url = 'http://twitter.com/statuses/update.json'
		values = {'status': 'This is an auto tweet sent at Unix time #1234567890. Rm\'ber this moment, it won\'t come again. May rock rule our <3s & geeks rule the world', 'source': 'filttr' }
		headers = {'Authorization': 'Basic ' + base64.b64encode('username:password')}

		data = urllib.urlencode(values)
		req = urllib2.Request(url, data, headers)
		response = urllib2.urlopen(req)
		exit()
	else:
		print t
		time.sleep(1)
	
