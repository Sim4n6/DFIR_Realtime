from flask import Flask, render_template
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
	search_tags = api.search("#DFIR", lang='en', rpp=30)
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

	auth = Auth(client_id, client_secret, redirect_uri, code=code)
	api = Api(auth)
	json_random_photo = api.photo.random()
	url_random_photo = json_random_photo['urls']['raw']
	print(url_random_photo)

	#return render_template("base.html", tweet=last_tweet.text, line=line, bg_photo=url_random_photo)
	return render_template("base.html")


if __name__ == '__main__':
	app.run()
