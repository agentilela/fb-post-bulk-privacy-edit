import os
import json
import string
import calendar
import time
from datetime import date
from httplib import *
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SINCE=calendar.timegm(date(2011,1,2).timetuple())
UNTIL=calendar.timegm(date(2018,1,1).timetuple())
INTERVAL=86400
privacy_setting='286958161406148' # only me

TOKEN=os.environ.get("TOKEN")
USER_ID=os.environ.get("USER_ID")
BODY=os.environ.get("BODY")
COOKIE=os.environ.get("COOKIE")

for cur_since in range(SINCE, UNTIL, INTERVAL):
    REQ_STRING='/me?access_token={TOKEN}&fields=posts.until({UNTIL}).since({SINCE})'.format(TOKEN=TOKEN,SINCE=cur_since, UNTIL=cur_since+INTERVAL,)
    print "Requesting {REQ_STRING}".format(REQ_STRING=REQ_STRING)
    conn = HTTPSConnection("graph.facebook.com")
    conn.request("GET", REQ_STRING)

    res = conn.getresponse()
    if res.status != 200:
        print "Get postids failed"
    #print res.read()
    d = json.load(res)

    if not 'posts' in d:
        print "No postids found between {SINCE} and {UNTIL}".format(SINCE=cur_since,UNTIL=cur_since+INTERVAL)
    else:
        for dd in d['posts']['data']:
            post_id = string.split(dd['id'], '_')[1]
            body = BODY
            header = {
                    "cookie": COOKIE,
                    "Content-type": "application/x-www-form-urlencoded",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
                    }
            conn2 = HTTPSConnection("www.facebook.com")
            conn2.request("POST", "/privacy/selector/update/?privacy_fbid="+post_id+
                "&post_param="+privacy_setting+
                "&render_location_enum=stream&is_saved_on_select=true&should_return_tooltip=false&prefix_tooltip_with_app_privacy=false&replace_on_select=false&dpr=1&ent_id="+post_id, body, header)

            res2 = conn2.getresponse()
        print "Setting "+post_id+" result code="+str(res2.status)
        if res2.status != 200 :
            print res2.read()
