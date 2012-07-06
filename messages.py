# Twitter profile image updater

# http://twitter.com/account/update_profile_image.json
# image = [imagefile]

import sys
import os
import random
import re
import urllib
import json
import codecs
import urllib2
import time
import oauth2 as oauth
import wcommon

def writelog(body):
	data = body
	if len(data) == 0:
		exit(0)
	log = codecs.getwriter('utf8')(open('messages.log', 'a'))
	if len(data) == 200:
		print >>log, "-- May have lost some tweets here [%s]" % (time.strftime("%a %b %d %H:%M:%S +0000 %Y"))
	for i in xrange(len(data)-1, -1, -1):
		tweet = data[i]
		link = "http://twitter.com/"+tweet['user']['screen_name']+"/status/"+str(tweet['id'])
		print >>log, "<%s> %s [%s] <%s>" % (tweet['user']['screen_name'], tweet['text'], tweet['created_at'], link)
	log.close()
	idfile = open('messages.id', 'w')
	print >>idfile, data[0]['id']
	idfile.close()
	

os.chdir("./logs/")

#Note: should not use exceptions here
# should be checking first if the file exists
lastid = None
try:
	lastid = open('messages.id', 'r').readline().strip()
except IOError:
	pass
if not lastid or lastid == '\n':
	try:
		log = open('messages.log', 'r')
		lasttweet = ""
		for line in log:
			lasttweet = line
		m = re.search(r"/status/(\d+)>", lasttweet)
		if not m:
			print "Problem with lastid"
			exit(1)
		lastid = int(m.group(1))
	except IOError:
		lastid = 12345 #fallback - download as many tweets as possible

received = 1
alldata = []
page = 1
while page < 2 or (received > 20 and page < 20):
	url = 'http://api.twitter.com/1/direct_messages.xml'
	head = ['Expect: ']
	data = [('count', 10)]
	#data = [('count', 200)]
	postdata = urllib.urlencode(data)
	url = url+'?'+postdata
	print url
	r, c = wcommon.oauth_req(url)
	if r.status > 200:
		print "Request failed: %d" % (r.status)
		sys.exit(1)
	print c
	jdata = json.loads(c)
	#print jdata
	alldata = alldata + jdata
	received = len(jdata)
	print str(received)+" messages"
	page += 1
	
writelog(alldata)

