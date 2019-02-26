import os

from flask import Flask, render_template
from flask_moment import Moment
from tweepy import API as tw_API
from tweepy import OAuthHandler
from unsplash.api import Api as us_API
from unsplash.auth import Auth

import tweepy

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

app = Flask(__name__)
moment = Moment(app)


@app.route("/")
def index():
	# Authentication and access to the API of Tweepy
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Search for the tag "DFIR" and get last_tweet 100 tweets in 01 page
	tweepy_api = tw_API(auth)
	tweets_search_4tag = tweepy_api.search("#DFIR", lang='en', rpp=100, tweet_mode="extended")

	# cursor on the search
	tweets_5 = []
	for status in tweepy.Cursor(tweepy_api.search, q="#DFIR", lang='en', rpp=100, tweet_mode="extended").items(5):
		tweets_5.append(status.full_text)

	# get last tweet
	last_tweet = tweets_search_4tag[0]
	tweet_text = last_tweet.full_text

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

	return render_template("base.html", tweet=tweet_text, tweets=tweets_5, bg_photo_url=bg_photo_custom_url)


if __name__ == '__main__':
	app.run()
