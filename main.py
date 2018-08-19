#!/usr/bin/python3
import configparser, twitter, subprocess

def email(mention):
	username = mention.user.screen_name
	tweet = mention.full_text

	subject = "@" + username + " mentioned us on twitter"
	message = "@" + username + ": " + tweet
	recipient = config["mail"]["recipient"]

	try:
		proc = subprocess.Popen(['mail', '-s', subject, recipient], stdin=subprocess.PIPE)
	except e:
		print(e)
	process.communicate(message)

try:
	latest = open("latest", "r")
except e:
	latest = open("latest", "w")
	latest.write(0)
	latest.close()
	latest = open("latest", "r")

number = int(latest.read())
latest.close()

config = configparser.ConfigParser()
config.read("twitter.config")

consumer_key = config["twitter"]["CONSUMER_KEY"]
consumer_secret = config["twitter"]["CONSUMER_SECRET"]
access_token_key = config["twitter"]["ACCESS_TOKEN_KEY"]
access_token_secret = config["twitter"]["ACCESS_TOKEN_SECRET"]

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret, tweet_mode="extended")

mentions = api.GetMentions()

max_number = number
for mention in mentions:
	if mention.id <= number:
		break
	else:
		if(mention.id > max_number)
			max_number = mention.id
		email(mention)

latest = open("latest", "w")
latest.write(max_number)
latest.close()