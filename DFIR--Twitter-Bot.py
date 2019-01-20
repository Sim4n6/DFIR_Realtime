from flask import Flask, render_template, url_for
from tweepy import API, OAuthHandler
from unsplash.api import Api
from unsplash.auth import Auth

import pprint
import os

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

app = Flask(__name__)


@app.route("/")
def index():

	# Authentication and access to the API
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Search for tag "DFIR" and get last_tweet
	api = API(auth)
	search_tags = api.search("#DFIR", lang='en', rpp=30, tweet_mode='extended')
	#pp = pprint.PrettyPrinter(indent=4)
	#pp.pprint(search_tags)

	# get last tweet
	last_tweet = search_tags[0]

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
	api = Api(auth)

	# Get a random photo object using the api
	bg_photo = api.photo.random()

	# Get URLs  of the random photo to be set
	bg_photo_urls = bg_photo[0].urls
	bg_photo_custom_url = bg_photo_urls.raw + "&fit=clamp&h=300&w=350&auto=compress"

	return render_template("base.html", tweet=last_tweet.full_text, line=line, bg_photo_url=bg_photo_custom_url)


if __name__ == '__main__':
	app.run()
