import json, requests,re
from dateutil import parser
import datetime
import time
from tweet import sendmessage
import os, sys
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nanoblog.settings")
sys.path.append(os.path.join(BASE_DIR,".."))
# This is so my local_settings.py gets loaded.
os.chdir(BASE_DIR)
# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from authentication.models import UserProfile,TweetUserLocation
from django.contrib.auth.models import User

def run():
	"""
	this sets up the server on the machine to periodically poll the loklak server and parse tweets accordingly
	"""
	user = "keepmesafe"
	last_retrieved_time = datetime.datetime.utcnow()
	url = "http://loklak.org/api/search.json?q=@"
	while True:
		time.sleep(3)
		t =last_retrieved_time.strftime("%Y-%m-%d_%H:%M")
		search_term = user+" since:"+t
		r = requests.get(url+search_term)
		print url+search_term,"polling!"
		while r.status_code != 200:
			r = requests.get(url+search_term)
		tweets = json.loads(r.content)["statuses"]
		if len(tweets) == 0:
			continue
		else:
			last_retrieved_time = parser.parse(tweets[0]["created_at"])
			last_retrieved_time = last_retrieved_time + datetime.timedelta(minutes =1)
			for tweet in tweets:
				if user not in tweet["mentions"]:
					print "continuing"
					continue
				# print tweet["mentions"]
				print 'Processing a tweet!', tweet["text"]
				to_reply = tweet["screen_name"].encode('utf-8')
				to_reply_id = tweet["id_str"].encode('utf-8')
				images_list = tweet["images"]
				tweet_text = tweet["text"].encode("utf-8")
				lat=""
				longt=""
				print tweet['location_point']
				if tweet['location_point']:
					location=tweet['location_point']
					print location[0]
					lat=location[0]
					longt=location[1]
				tweet_text = tweet_text.split()
				tweet_email=tweet_text[1]
				t=TweetUserLocation()
				t.screen_name=to_reply
				t.latitude=lat
				t.longt=longt
				t.save()
				msg = "We have recorded your response thanks"
				if msg != "":
					sendmessage(to_reply,msg, to_reply_id)
					print 'Replied to', to_reply,"!"

if __name__ == '__main__':
	run()