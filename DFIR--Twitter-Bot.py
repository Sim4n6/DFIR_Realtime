from flask import Flask
from tweepy import API,OAuthHandler

from keys import consumer_key,consumer_secret, access_token,access_token_secret

app = Flask(__name__)


@app.route("/")
def index():

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = API(auth)

	public_tweets = api.home_timeline()
	for tweet in public_tweets:
		print(tweet.text)

	return "Hello World!" + str(tweet.text)


if __name__ == '__main__':
	app.run()
