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

	
def encode_file_data(image):
	boundary = hex(int(time.time()))[2:]
	headers = {}
	headers['Content-Type'] = 'multipart/form-data; boundary="%s"' % (boundary)
	data = [] #to be joined later (faster)
	data.append("--"+boundary)
	data.append("\r\n")
	data.append('Content-Disposition: form-data; name="image"; filename="%s"\r\n' % image.name)
	if image.name.endswith("jpg") or image.name.endswith("jpeg"):
		data.append("Content-Type: image/jpeg\r\n\r\n")
	elif image.name.endswith("png"):
		data.append("Content-Type: image/png\r\n\r\n")
	elif image.name.endswith("gif"):
		data.append("Content-Type: image/gif\r\n\r\n")
	else:
		data.append("Content-Type: application/octet-stream\r\n\r\n")
	data.append(image.read())
	data.append("\r\n--")
	data.append(boundary)
	data.append("--\r\n\r\n")
	body = ''.join(data)
	headers['Content-Length'] = str(len(body))
	return (headers, body)
	

os.chdir("./pics/")
files = os.listdir(os.getcwd())
images = []
for filename in files:
	if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".gif"):
		images.append(filename)
imagefile = random.choice(images)
image = open(imagefile, 'r')

url = 'http://api.twitter.com/1/account/update_profile_image.json'
headers, postdata = encode_file_data(image)
r, c = wcommon.oauth_req(url, http_method="POST", post_body=postdata, http_headers=headers)
if r.status != 200:
	print "Updating profile image did not succeed: Status %d" % (r.status)

