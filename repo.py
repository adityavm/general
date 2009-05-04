# -*- coding: UTF-8 -*-

# Personal Code-Bits Repo Using Python and Delicious
# --------------------------------------------------

import urllib
import urllib2
import time
import sys
from xml.dom.minidom import parseString

_user = ''
_pass = ''
_url = 'api.del.icio.us'
_url_str = 'http://adityamukherjee.com/'

keychain = urllib2.HTTPPasswordMgrWithDefaultRealm()
keychain.add_password('del.icio.us API', _url, _user, _pass)
handle = urllib2.HTTPBasicAuthHandler(keychain)
opener = urllib2.build_opener(handle)
urllib2.install_opener(opener)

def getPost(tags):
	tags = tags.replace('+', " ")
	return urllib2.urlopen('https://' + _url + '/v1/posts/recent?tag=' + urllib.quote(tags))

def addPost(tags, upd, url):
	stamp = int(time.time())
	
	if(url != ''):
		url_string = url
	else:
		url_string = _url_str + str(stamp)
	
	params = urllib.urlencode({
		'shared':'no', 
		'replace':'yes', 
		'tags': tags.replace("+", " "), 
		'url': url_string,
		'description': 'Repository entry: ' + tags.replace('repo', "").replace('+', ' ').strip(),
		'extended': upd
	})
	#print params
	return urllib2.urlopen("https://" + _url + "/v1/posts/add?%s" % params)

inp = raw_input(": ")
inp = inp.split(' ')
while(inp[0] != 'exit'):
	tags = 'repo ' + inp[1]
	
	if(inp[0] == 'put'):
		stat = ' '.join(inp[2:len(inp)])
		
		dom = parseString(getPost(tags).read())
		post = dom.getElementsByTagName('post')
		if(post.length):
			e = post[0] # get the first
			if(e.getAttribute('href')):
				url = e.getAttribute('href')
			desc = (time.strftime('%I:%M%p/%d.%m').lower() + ": " + stat + "\n" + e.getAttribute('extended')).strip()
		else:
			url = ''
			desc = (time.strftime('%I:%M%p/%d.%m').lower() + ": " + stat).strip()
		
		result = parseString(addPost(tags, desc, url).read()) # make the call
		print "<" + result.getElementsByTagName('result')[0].getAttribute('code') + ">"
	
	elif(inp[0] == 'rem'):
		dom = parseString(getPost(tags).read())
		post = dom.getElementsByTagName('post')
		if(post.length):
			e = post[0]
			note = e.getAttribute('extended')
			notes = note.split("\n")
			#print(notes)
			note = "\n".join(notes[1:len(notes)])
			addPost(e.getAttribute('tag'), note, e.getAttribute('href'))
		else:
			print "<no entries>"	
		
	else:
		dom = parseString(getPost(tags).read())
		post = dom.getElementsByTagName('post')
		if(post.length):
			e = post[0]
			print e.getAttribute('description') + "\n" + '-'*len(e.getAttribute('description')) + '\n'
			print e.getAttribute('extended')
		else:
			print "<no entries>"
			
	inp = raw_input(": ") # ask again
	inp = inp.split(' ')