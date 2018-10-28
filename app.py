from flask import Flask, render_template
from flask_ask import Ask, statement, question
from datetime import datetime
import json
import random
import feedparser

# --------------------------------------------------------------------------------------------
# INITIALISATION

app = Flask(__name__)
ask = Ask(app, "/alexa")

song_url = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=25/xml"
tvShow_url = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topTvSeasons/xml"
song_list = ["songs","song","music","soundtrack","album","albums","soundtracks"]
tvShow_list = ["tvshows","tvseries","series","seasons","tv","episodes","shows"]


@ask.launch
def new_ask():
    print("Launch invoked")
    welcome = "Welcome to the Itune feeds.\n\n Get to know the top rated tv shows and songs, their price, genre and related data just by saying 'show me the top Songs or Top Series'"
    return question(welcome)


@ask.intent("top_songs_shows")
def top_songs_shows(category):
	category = category.lower()
	if category in song_list:
		url = song_url
	elif category in tvShow_list:
		url = tvShow_url
	else:
		return question("Sorry the following category doesn't exist.\n\n Say 'top songs' or 'top series' ")	

	reply = "The top " + category + " are as follows: \n\n"
	entry_list = get_rss_data(url, category)
	for index, entry in enumerate(entry_list):
		print(entry)
		reply += str(index+1) + " \n\n" + entry["name"] + "\n\nIts Genre is " + entry["genre"] + "\n\nIts Price is $" + entry["price"] +  "\n\nIts Release Date is " + entry["releaseDate"] + "\n\n"

	return question(reply)	
		

def get_rss_data(url,category):
	entry_list = []
	data = feedparser.parse(url)
	entries = data["entries"]
	for entry in entries:
		entry_info = {}

		if category in tvShow_list:
			name = entry["im_name"]
		else:
			name = entry["title"]

		#print("Name : " + name)
		
		genre = entry["tags"][0]["label"]
		#print("Genre : " + genre)

		releaseDate = entry["im_releasedate"]["label"]
		#print("Release Date : " + releaseDate)

		price = entry["im_price"]["amount"]
		#print("Price : " + price)
		
		entry_info["name"] = name
		entry_info["genre"] = genre
		entry_info["releaseDate"] = releaseDate
		entry_info["price"] = price

		entry_list.append(entry_info)	

	return entry_list	


@ask.intent("AMAZON.FallbackIntent")
def fallback():
	reply = "I didn't understand you.\n Say Top shows on itunes or Top songs on itunes to get highest rated songs and shows from itunes."
	return question(reply)


@ask.intent("AMAZON.CancelIntent")
def cancel():
	reply = "Closing the feeds."
	return statement(reply)


@ask.intent("AMAZON.StopIntent")
def fallback():
	reply = "Closing the feeds."
	return statement(reply)


@ask.intent("AMAZON.HelpIntent")
def fallback():
	reply = "I didn't understand you.\n Say Top shows on itunes or Top songs on itunes to get highest rated songs and shows from itunes."
	return question(reply)


@ask.intent("AMAZON.NavigateHomeIntent")
def fallback():
	reply = "Closing the feeds."
	return statement(reply)


@app.route("/", methods=["GET", "POST"])
def index():
	print("Home Page")
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0",threaded=True)