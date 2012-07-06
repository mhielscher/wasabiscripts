#!/usr/bin/python

import urllib2
import json
import time
import sys
import oauth2 as oauth
import wcommon

url = "http://api.twitter.com/1/account/rate_limit_status.json"

#wcommon.getConsumerPair()
#wcommon.getUserPair("WasabiFlux")

if len(sys.argv) < 2 or sys.argv[1] != '-ip':
	print "Checking by username..."
	r, c = wcommon.oauth_req(url)
	if r.status > 200:
		print "Request failed: %d" % (r.status)
		sys.exit(1)
else:
	print "Checking by IP..."
	f = wcommon.openUrlSafe(url)
	c = f.read()

data = json.loads(c)

#print c
print "Remaining requests: %s" % data['remaining_hits']
print "Hourly limit: %s" % data['hourly_limit']
print "Reset time: %s" % (time.strftime("%H:%M:%S", time.localtime(int(data['reset_time_in_seconds']))))
