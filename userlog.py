# Twitter profile image updater

# http://twitter.com/account/update_profile_image.json
# image = [imagefile]

import sys
import os
import pycurl
import random
import re
import urllib
import json
import codecs
import smtplib
import urllib2
import time
import oauth2 as oauth
import wcommon

targetuser = sys.argv[1]

def writelog(body, logname):
	#tj = codecs.getwriter('utf8')(open('timeline.json', 'a'))
	#print >>tj, body
	#tj.close()
	#data = json.loads(body)
	data = body
	if len(data) == 0:
		exit(0)
	log = codecs.getwriter('utf8')(open(logname+".log", 'a'))
	#if len(data) == 200:
	#	print >>log, "-- May have lost some tweets here [%s]" % (time.strftime("%a %b %d %H:%M:%S +0000 %Y"))
	for i in xrange(len(data)-1, -1, -1):
		tweet = data[i]
		link = "http://twitter.com/"+tweet['user']['screen_name']+"/status/"+str(tweet['id'])
		print >>log, "<%s> %s [%s] <%s>" % (tweet['user']['screen_name'], tweet['text'], tweet['created_at'], link)
	log.close()
	idfile = open(logname+".id", 'w')
	print >>idfile, data[0]['id']
	idfile.close()


os.chdir("./logs/")

#Note: should not use exceptions here
# should be checking first if the file exists
lastid = None
try:
	lastid = open(targetuser+'.id', 'r').readline().strip()
except IOError:
	pass
if not lastid or lastid == '\n':
	try:
		log = open(targetuser+'.log', 'r')
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

print "Retrieving timeline for "+targetuser+"..."
received = 1
alldata = []
page = 1
while received > 0 and page < 20:
	print "Grabbing page "+str(page)+": ",
	url = 'http://api.twitter.com/1/statuses/user_timeline.json'
	head = ['Expect: ']
	#data = [('since_id', lastid), ('count', 20)]
	data = [('screen_name', targetuser), ('count', 200), ('page', page)]
	postdata = urllib.urlencode(data)
	url = url+'?'+postdata
	r, c = wcommon.oauth_req(url)
	jdata = json.loads(c)
	#print jdata
	alldata = alldata + jdata
	received = len(jdata)
	print str(received)+" tweets"
	page += 1

writelog(alldata, targetuser)
