from engine import getJson, shorten, getBeatifulXML
import config, magic, urllib, config, re

def lastfm(q_query, raw_query, page):
	results = []
	j = getJson("http://ws.audioscrobbler.com/2.0/?method=artist.search&artist=%s&api_key=%s&format=json&limit=3" % (q_query, config.lastfm_key))
	if "artist" in j['results']['artistmatches']:
		for artist in j['results']['artistmatches']['artist']:
			for th in artist['image']:
				if th['size'] == "large":
					t = th['#text']
			results.append({
				"style" : "lastfm music",
				"title" : artist['name'],
				"url" : artist['url'],
				"display_url" : artist['url'],
				"snippet" : '<img src="%s" />' % t
			})
	return results

def jpopasia(q_query, raw_query, page):
	'''
	Note: Must be activated in config
	'''
	results = []
	j = getBeatifulXML("http://www.jpopasia.com/search/?q=%s" % q_query)
	for link in j.find("div", **{"class" : "content box"}).findAll("a", href= re.compile( "^" + re.escape("http://www.jpopasia.com/group") ) ):
		# Now we have a link to all of the content
		p = getBeatifulXML(link['href'])
		results.append({
			"style" : "jpopasia music fullscreen",
			"title" : p.find("title"),
			"url" : link['href'],
			"display_url" : link['href'],
			"snippet" : p.find(**{"class" : "c66" }).find("div", **{"class" : "content box"})
		})
	return results
