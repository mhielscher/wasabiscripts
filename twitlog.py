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
	log = codecs.getwriter('utf8')(open('timeline.log', 'a'))
	if len(data) == 200:
		print >>log, "-- May have lost some tweets here [%s]" % (time.strftime("%a %b %d %H:%M:%S +0000 %Y"))
	for i in xrange(len(data)-1, -1, -1):
		tweet = data[i]
		link = "http://twitter.com/#!/"+tweet['user']['screen_name']+"/status/"+str(tweet['id'])
		text = "<%s> %s [%s] <%s>" % (tweet['user']['screen_name'], tweet['text'], tweet['created_at'], link)
		if 'entities' in tweet and 'urls' in tweet['entities']:
			for url in tweet['entities']['urls']:
				if url['url'] and url['expanded_url']:
					text = text.replace(url['url'], url['expanded_url'])
		print >>log, text
	log.close()
	idfile = open('timeline.id', 'w')
	print >>idfile, data[0]['id']
	idfile.close()


os.chdir("./logs/")

#Note: should not use exceptions here
# should be checking first if the file exists
lastid = None
try:
	lastid = open('timeline.id', 'r').readline().strip()
except IOError:
	pass
if not lastid or lastid == '\n':
	try:
		log = open('timeline.log', 'r')
		lasttweet = ""
		for line in log:
			lasttweet = line
		m = re.search(r"/status/(\d+)>", lasttweet)
		if not m:
			print "Problem with lastid"
			exit(1)
		lastid = int(m.group(1))
	except IOError:
		lastid = 123456 #fallback - download as many tweets as possible

received = 1
alldata = []
page = 1
while page < 2 or (received > 20 and page < 20):
	url = 'http://api.twitter.com/1/statuses/home_timeline.json'
	head = ['Expect: ']
	data = [('include_entities', True), ('since_id', lastid), ('count', 200), ('page', page)]
	#data = [('count', 200)]
	postdata = urllib.urlencode(data)
	url = url+'?'+postdata
	r, c = wcommon.oauth_req(url)
	if r.status > 200:
		print "Request failed: %d" % (r.status)
		sys.exit(1)
	jdata = json.loads(c)
	#print jdata
	alldata = alldata + jdata
	received = len(jdata)
	print str(received)+" tweets"
	page += 1

writelog(alldata)

