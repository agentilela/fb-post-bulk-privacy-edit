## Introduction

Facebook has a tool in settings page, it can bulk modify post privacy settings for old posts, the tool is called "Limit old posts".

However, the tool can only modify posts that are shared with "Public" or "Friends of friends". So my script attempts to solve this problem.

**Warning: this is a super hacky proof of concept project that contains a lot of dirty and badly written code, but hey, it works for me.**

## How it works

Facebook Graph API does not offer a way to modify post privacy settings, so my script needs you to steal cookies from a logged in browser, and send resuests emulating the browser to modify post privacy settings.

## How do I use it? (for people not familiar with commandline operations)

### Setup Python / Workspace

1. You need to have Python 2 on your computer, modern MacOS and many Linux distributions have it.
2. Download the code from Github, unzip, open a terminal, navigate to the unzipped folder by typing `cd`, space, then drag the unzipped folder onto the terminal window.

### Setup Keys

3. Create a file called `.env` in the same directory where you unzipped the code.
4. Open the file with a text editor, and copy and paste the following into it:

```
USER_ID=""

BODY=""

COOKIE=""

TOKEN=""
```

5. Keep the file open and fill in the parameters with the following data:

* USER_ID
  * [Find your facebook ID](https://findmyfbid.com/), it should be a long number.
  * Copy and paste this number into the USER_ID parameter (e.g. `USER_ID="12345678"`).
* BODY
  * Open [your facebook profile page](https://www.facebook.com/me), [open developer tools](https://developer.chrome.com/devtools#access), switch to the "Network" tab, input `/privacy/selector/update/` into the filter field.
  * Open any of your facebook posts, change its privacy settings to anything, and switch it back, a few entries should appear on in the "Network" tab.
  * Click any entry starting with `?privacy_fbid`. A panel will open to the right.
  * Scroll down to find "Form Data" section, click "view source", copy all the text.
  * Paste this text into the BODY parameter (e.g. `BODY="\_\_user=1234567&....."`).
* COOKIE
  * In same `privacy_fbid` panel from above, scroll down and find the "Request Headers" section.
  * In the section find the `cookie:` field, copy all the text.
  * Paste this text into the COOKIE parameter (e.g. `COOKIE="datr=asgsagjhu12521;....."`).
* TOKEN
  * [API Explorer](https://developers.facebook.com/tools/explorer), click "Obtain Token", then "Obtain User Access Token", check `user_posts`, click "Obtain Access Token".
  * Copy the text in the field "Access Token", it usually starts with `EAACE....`.
  * Paste this text into the TOKEN parameter (e.g. `TOKEN="EAACEdEose....."`).

6. Save and close the `.env` file.

### Run

6. Open `process.py` using a text editor.
7. Edit the date numbers in which your posts' privacy settings will be edited, using the `SINCE` and `UNTIL` parameter.
   * For example: `SINCE=calendar.timegm(date(2011,8,1).timetuple())` this would mean to modify all posts **since** 2011/8/1.
8. Save and close the `process.py` file.
9. Switch to the terminal window that you opened in step 2, type in `python process.py`, hit enter, and the script will start to run, if you see something like `Setting 64123317123111234 result code=200`, the script is running successfully. (result code 200 mean success, otherwise failure). You can hit Ctrl+C to stop the script any time.

## process.py

This script first uses Graph API to grab all post ID's from a specific timeframe, then emulate browser requests to each of them.

However, I found that the wacky [Graph API /user_id/posts endpoint does not actually show all posts](https://stackoverflow.com/questions/7659701/facebook-graph-api-json-missing-posts), so there needs to be another way to grab all post IDs.

### Parameters:

`TOKEN`: a valid Facebook OAuth client token that is authorized to read your own timeline, you can go to [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer), click "Get Token", authorize it with `user_posts` permission, and copy the token here.

`privacy_setting`: target privacy setting you wish to set. You can use `286958161406148` for "Only me". To use other values, open your browser developer console's network tab, then change privacy setting to what you want (Friends, Public, Custom list, etc) for an arbitrary post, monitor the dev console for xhr POST request to `/privacy/selector/update/`, inside the request HTTP query strings, `post_param` is the id for that privacy setting. Set this `privacy_setting` to the privacy setting id you want to use.

`BODY`: also from the request intercepted above, copy the request body here. It usually starts with `__user=....`.

`COOKIE`: steal cookies also from that intercepted request, you can find it in `cookie` request header.

## process_from_ids.py

One way to grab all post IDs is:

1. Open your profile page on a browser
2. Find something small and heavy to keep your `End` key (`Fn+Down` for Mac) pressed down
3. Go to lunch
4. In the browser, save the page
5. Use the following command to get all post IDs that is on the saved HTML page:

   egrep -oh 'top_level_post_id&quot;:&quot;(\d+)&quot;' Your_page.html | cut -c 31-45

6. Save post IDs to a file `post_ids`

Then, `process_from_ids.py` can read post IDs from that file and modify privacy settings for them.

_Note: maybe later I can use Casperjs to grab the post IDs, maybe even get cookie by emulating login on Casperjs_

## License

AGPLv3
