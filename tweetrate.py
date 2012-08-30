#!/usr/bin/python

import datetime
import sys
import re

if len(sys.argv) < 3:
	print "Please specify a username and log file."
	sys.exit(1)

user = sys.argv[1]

logfile = sys.argv[2]
log = open(logfile, 'r')

timestampregex = re.compile(r"\[([^\]]+)\] <.*>")
usernameregex = re.compile(r"^<"+user+r">")

tweets = [t for t in log if usernameregex.match(t)]
print len(tweets)

rate = dict()
for t in tweets:
    timestamp = "now"
    try:
        timestamp = timestampregex.search(t).group(1)
        #print timestamp
    except AttributeError:
        continue
    otm = datetime.datetime.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y")
    td = datetime.timedelta(hours=-8)
    tm = otm + td
    #print tm
    day = tm.date()
    if day not in rate.keys():
        rate[day] = 1
    else:
        rate[day] = rate[day]+1

span = sorted(rate.keys())
for day in span:
	print "%s,%d" % (day, rate[day])
#startdate = datetime.date(*[int(n) for n in span[0].split('-')])
#enddate = datetime.date(*[int(n) for n in span[-1].split('-')])
days = (span[-1] - span[0]).days
print "Average: %.1f tweets per day" % (sum(rate.values())/days)
