import time
import json
import sys
import urllib2
import oauth2 as oauth

CONSUMER_KEY = None
CONSUMER_SECRET = None
USER_KEY = None
USER_SECRET = None

def getConsumerPair():
	#this is a temporary implementation
	global CONSUMER_KEY
	global CONSUMER_SECRET
	consumerFile = open("consumer.txt", 'r')
	CONSUMER_KEY = consumerFile.readline().rstrip('\n')
	CONSUMER_SECRET = consumerFile.readline().rstrip('\n')
	consumerFile.close()
	return (CONSUMER_KEY, CONSUMER_SECRET)
	
def getUserPair(user):
	#this is a temporary implementation
	global USER_KEY
	global USER_SECRET
	userFile = open("user.txt", 'r')
	USER_KEY = userFile.readline().rstrip('\n')
	USER_SECRET = userFile.readline().rstrip('\n')
	userFile.close()
	return (USER_KEY, USER_SECRET)

#temporary
getConsumerPair()
getUserPair(None)

def openUrlSafe(url):
	f = None
	clock = 0
	while not f and clock < 30:
		try:
			f = urllib2.urlopen(url)
		except urllib2.HTTPError, e:
			if e.code == 401:
				printAuthWrong()
				sys.exit(0)
			elif e.code == 500:
				clock += 10
				time.sleep(10)
			elif e.code == 502 or e.code == 503:
				clock += 5
				time.sleep(5)
	return f
	
def oauth_req(url, key=USER_KEY, secret=USER_SECRET, http_method="GET", post_body='', http_headers=None):
	global CONSUMER_KEY
	global CONSUMER_SECRET
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth.Token(key=key, secret=secret)
	client = oauth.Client(consumer, token)

	resp = None
	content = None
	clock = 0
	while content == None or (clock < 60 and resp.status >= 500):
		resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
		if resp.status == 500:
			clock += 10
			time.sleep(10)
		elif resp.status == 502 or resp.status == 503:
			clock += 5
			time.sleep(5)
		#print resp.status, clock
	return resp, content


