# Twitter profile image updater

# http://twitter.com/account/update_profile_image.json
# image = [imagefile]

import sys
import os
import random
import re
import urllib
import json
import urllib2
import oauth2 as oauth
import time
import wcommon

status = None

if len(sys.argv) < 2 or sys.argv[1] == "-i": #interactive mode
	while not status:
		status = raw_input("Enter your status: ")
		if len(status) > 140:
			print "Status is %d characters. Limit is 140." % (len(status))
elif len(sys.argv) > 1:
	status = sys.argv[1]
else:
	sys.exit(1)


url = 'http://api.twitter.com/1/statuses/update.xml'
data = [('status', unicode(status)), ('include_entities', True)]
postdata = urllib.urlencode(data)
r, c = wcommon.oauth_req(url, http_method="POST", post_body=postdata)
if r.status != 200:
	print "Setting status did not succeed: Status %d" % (r.status)
print c

