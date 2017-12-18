"""Batch Update FB Post Privacy."""
import calendar
import json
import string
from datetime import date
from httplib import HTTPSConnection
from os import environ
from os.path import dirname, join
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

# Config
PRIVACY_SETTING = '286958161406148'  # only me
TOKEN = environ.get("TOKEN")
USER_ID = environ.get("USER_ID")
BODY = environ.get("BODY")
COOKIE = environ.get("COOKIE")
SINCE = calendar.timegm(date(2008, 1, 2).timetuple())
UNTIL = calendar.timegm(date(2018, 1, 1).timetuple())

# HTTP Settings
UPDATE_PATH = '/privacy/selector/update/'
URL_PARAMS_1 = "is_saved_on_select=true&should_return_tooltip=false"
URL_PARAMS_2 = "prefix_tooltip_with_app_privacy=false&replace_on_select=false&dpr=1"
LOCATION = 'stream'
CONTENT_TYPE = "application/x-www-form-urlencoded"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
HEADER = {
    "cookie": COOKIE,
    "Content-type": CONTENT_TYPE,
    "user-agent": USER_AGENT
}


def set_privacy(post_id):
    """Set privacy of a single post."""
    raw_update_url = "{a}?privacy_fbid={b}&post_param={c}&render_location_enum={d}&{e}&ent_id={b}"
    update_url = raw_update_url.format(
        a=UPDATE_PATH, b=post_id, c=PRIVACY_SETTING, d=LOCATION, e=URL_PARAMS_1 + URL_PARAMS_2, )
    print "Calling URL {URL}".format(URL=update_url)
    conn2 = HTTPSConnection("www.facebook.com")
    conn2.request("POST", update_url, BODY, HEADER)
    res2 = conn2.getresponse()
    raw_output = "Setting {post_id} result code: {STATUS}"
    print raw_output.format(post_id=post_id, STATUS=res2.status)


def update_posts(posts):
    """Loop through posts."""
    if not 'data' in posts:
        raw_error = "No postids found {posts}"
        print raw_error.format(posts=json.dumps(posts, indent=4, sort_keys=True))
    else:
        print "Updating {len} posts ".format(len=len(posts['data']))
        for parsed_post in posts['data']:
            post_id = string.split(parsed_post['id'], '_')[1]
            set_privacy(post_id)
        if 'paging' in posts and 'next' in posts['paging']:
            next_url = posts['paging']['next']
            print "got next url {next_url}".format(next_url=next_url)
            next_responses = collect_posts(next_url)
            update_posts(next_responses)


def collect_posts(collect_url):
    """Get posts from url."""
    conn = HTTPSConnection("graph.facebook.com")
    conn.request("GET", collect_url)

    res = conn.getresponse()
    if res.status != 200:
        print "Get postids failed {STATUS}".format(STATUS=res.status)
    else:
        return json.load(res)


def main():
    """Main Loop."""
    raw_collect_url = '/me?access_token={TOKEN}&fields=posts.until({UNTIL}).since({SINCE})'
    collect_url = raw_collect_url.format(TOKEN=TOKEN, SINCE=SINCE, UNTIL=UNTIL)
    print "Requesting {collect_url}".format(collect_url=collect_url)

    parsed_responses = collect_posts(collect_url)
    if parsed_responses and 'posts' in parsed_responses:
        update_posts(parsed_responses['posts'])
    else:
        raw_error = "No postids found {parsed_responses} at ${collect_url}"
        pretty_responses = json.dumps(
            parsed_responses, indent=4, sort_keys=True)
        print raw_error.format(parsed_responses=pretty_responses, collect_url=collect_url)


main()
