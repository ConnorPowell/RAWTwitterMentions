import configparser, twitter, subprocess, psycopg2, time

def email(mention, cursor):
	username = mention.user.screen_name
	tweet = mention.full_text

	subject = "@" + username + " just mentioned us on twitter"
	message = "@" + username + ": " + tweet
	sender = mention.user.name + " <notify@twitter.com>"
	timestamp = int(time.time())

	cursor.execute("INSERT INTO email (new_flag, datetime, sender, subject, body) VALUES (%s, %s, %s, %s, %s)",
		("t", timestamp, sender, subject, message))
	print("Inserted", subject, message, "", sep="\n")
	
latest = open("latest", "r")
number = int(latest.read())
latest.close()

config = configparser.ConfigParser()
config.read("twitter.config")

db_host = config["database"]["host"]
db_port = config["database"]["port"]
db_name = config["database"]["name"]
db_user = config["database"]["user"]
db_password = config["database"]["password"]

connection = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cursor = connection.cursor()

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
		if mention.id > max_number:
			max_number = mention.id
		email(mention, cursor)

connection.commit()
cursor.close()
connection.close()

latest = open("latest", "w")
latest.write(str(max_number))
latest.close()