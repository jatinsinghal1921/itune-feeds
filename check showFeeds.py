import feedparser


def get_rss_data(url,category):
	entry_list = []
	data = feedparser.parse(url)
	entries = data["entries"]
	for entry in entries:
		entry_info = {}

		if category == "tv":
			name = entry["im_name"]
		else:
			name = entry["title"]
			
		print("Name : " + name)
		
		genre = entry["tags"][0]["label"]
		print("Genre : " + genre)

		releaseDate = entry["im_releasedate"]["label"]
		print("Release Date : " + releaseDate)

		price = entry["im_price"]["amount"]
		print("Price : " + price)
		
		entry_info["name"] = name
		entry_info["genre"] = genre
		entry_info["releaseDate"] = releaseDate
		entry_info["price"] = price

		entry_list.append(entry_info)	

	return entry_list



url = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topTvSeasons/xml"
url = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=25/xml"
show_list = get_TVshow_data(url,"song")
for show in show_list:
	print("********************************************")
	print("Name : " + show["name"])
	print("Genre : " + show["genre"])
	print("Price : " + show["price"])
	print("Release Date : " + show["releaseDate"])
	
