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

tweetid = None

if len(sys.argv) == 2:
	tweetid = sys.argv[1] #string
else:
	print "Specify tweet ID."
	sys.exit(1)

url = 'http://api.twitter.com/1/statuses/show.xml'
head = ['Expect: ']
data = [('id', tweetid), ('include_entities', True)]
postdata = urllib.urlencode(data)
url = url+'?'+postdata
r, c = wcommon.oauth_req(url)
if r.status != 200:
	print "Could not retrieve tweet: Status %d" % (r.status)
print c

