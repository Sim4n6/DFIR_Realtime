from flask import Flask
from tweepy import API, OAuthHandler

from keys import consumer_key, consumer_secret, access_token, access_token_secret

app = Flask(__name__)


@app.route("/")
def index():

	# Authentication and access to the API
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Search for tag "DFIR" and get last_tweet
	api = API(auth)
	search_tags = api.search("#DFIR")
	last_tweet = search_tags[0]

	# store id of last_week_tweet in a file
	with open("last_week_id.txt", 'w') as lst_hd:
		lst_hd.write(str(last_tweet.id))

	# Read last_week_tweet from a file
	with open("last_week_id.txt") as lst_hd:
		line = int(lst_hd.read())

	return "Hello World! <br> >" + str(last_tweet.text) + "<br> >" + str(line)


if __name__ == '__main__':
	app.run()
