from flask import Flask, render_template, url_for
from tweepy import API as tw_API
from tweepy import OAuthHandler
from unsplash.api import Api as us_API
from unsplash.auth import Auth
from datetime import datetime as dt

import pprint
import os

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

app = Flask(__name__)


@app.route("/")
def index():

	# Authentication and access to the API of Tweepy
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Search for the tag "DFIR" and get last_tweet 100 tweets in 01 page
	tweepy_api = tw_API(auth)
	tweets_search_4tag = tweepy_api.search("#DFIR", lang='en', rpp=100, page=1, tweet_mode="extended")
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(tweets_search_4tag)

	# cursor on the search
	for status in tweepy_api.Cursor(tweepy_api.search("#DFIR", lang='en', rpp=100, page=1, tweet_mode="extended")).items():
		pp.pprint(">>", status)

	# get last tweet
	last_tweet = tweets_search_4tag[0]
	tweet_text = last_tweet.full_text

	# store id of last_week_tweet in a file
	with open("last_week_id.txt", 'w') as lst_hd:
		lst_hd.write(str(last_tweet.id))

	# Read last_week_tweet from a file
	with open("last_week_id.txt") as lst_hd:
		line = int(lst_hd.read())

	client_id = os.environ['access_key_unsplash']
	client_secret = os.environ['secret_key_unsplash']
	redirect_uri = os.environ['redirect_uri_unsplash']
	code = os.environ['code_unsplash']

	# Authentication and api instanciation
	auth = Auth(client_id, "", "", "")
	unsplash_api = us_API(auth)

	# Get a random photo object using the api
	bg_photo = unsplash_api.photo.random()

	# Get URLs  of the random photo to be set
	bg_photo_urls = bg_photo[0].urls
	bg_photo_custom_url = bg_photo_urls.raw + "&fit=clamp&h=300&w=350&auto=compress"

	# Get now() datetime
	now_dt = dt.now()

	return render_template("base.html", tweet=tweet_text, line=line, bg_photo_url=bg_photo_custom_url, date_time=now_dt)


if __name__ == '__main__':
	app.run()
