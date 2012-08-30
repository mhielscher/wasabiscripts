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

tweetid = None

if len(sys.argv) < 2 or sys.argv[1] == "-i": #interactive mode
    while not tweetid:
        try:
            tweetid = long(raw_input("Tweet ID to RT: "))
        except ValueError:
            continue
elif len(sys.argv) > 1:
    tweetid = long(sys.argv[1])
else:
    sys.exit(1)
        

url = "http://api.twitter.com/1/statuses/retweet/%d.xml" % (tweetid)
data = []
postdata = urllib.urlencode(data)
r, c = wcommon.oauth_req(url, http_method="POST", post_body=postdata)
if r.status != 200:
    print "Retweeting did not succeed: Status %d" % (r.status)
    print c
    sys.exit(r.status)


