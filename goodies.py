def intToBinary(query):
	try:
		result = int2bin(int(query))
	except ValueError:
		result = ''
		for c in query:
			result += bin(ord(c))[2:]
	return {
		"style" : "goodies",
		"title" : "Base-10 (Deanary) to Base-2 (Binary)",
		"snippet" : "%s is %s" % (query, result)
	}

def int2bin(n, digits=8):
    rep = bin(n)[2:]
    return ('0' * (digits - len(rep))) + rep

def dictionary(query):
	import config, engine, urllib2
	from BeautifulSoup import BeautifulSoup
	j = urllib2.urlopen("http://api-pub.dictionary.com/v001?vid=%s&q=%s&type=define" % ( config.dictionary_com_key, query ))
	j = BeautifulSoup(j)
	d = None
	try:
		d = j.find("def").contents[0] + ""
	except Exception:
		pass

	if d is not None:
		return {
			"style" : "goodies",
			"title" : "Dictionary.com defention of %s" % query,
			"snippet" : d,
			"url" : "http://dictionary.com",
			"display_url" : "Powered by Dictionary.com"
		}
	else:
		j = engine.getJson("http://www.urbandictionary.com/iphone/search/define?term=%s" % query)
		if j['result_type'] != "no_results":
			d = j['list'][0]
			s = '<strong>%s</strong>: %s<br/>Examples: %s' % ( d['word'], d['definition'].replace("\n", "<br/>"), d['example'].replace("\n", "<br/>") )
			return {
				"style" : "goodies",
				"title" : "UrbanDictionary defention of %s" % query,
				"snippet" : s,
				"url" : "http://urbandictionary.com",
				"display_url" : "Powered by UrbanDictionary.com"
			}

def random(query):
	if query == "word":
		import config, engine		
		j = engine.getXML("http://api-pub.dictionary.com/v001?vid=%s&type=random" % config.dictionary_com_key, fresh=True)
		return {
			"style" : "goodies",
			"title" : "Random Word",
			"snippet" : '<a href="?q=define %(word)s" title="Find out the defenition">%(word)s</a>' % { "word" : j.findtext("random_entry") },
			"url" : "http://dictionary.com",
			"display_url" : "Powered by Dictionary.com"
		}
	import re, random
	s = re.search('.*' + re.escape("between") + ' ?([0-9]+) ?' + re.escape("and") + ' ?([0-9]+)', query)
	if s != None:
		a = int(s.group(1))
		b = int(s.group(2))
		if a > b:
			c = b
			b = a
			a = c
		return {
			"style" : "goodies",
			"title" : "Random number",
			"snippet" : "A random number between %s and %s is %s" % (a, b, random.randint(a, b))
		}
	return None
	
def pythonLib(query):
	try:
		module = __import__(query)
		s = ''
		if module.__doc__:
			s = module.__doc__.replace("\n", "<br/>")
		return {
			"style" : "goodies fullscreen",
			"title" : "Python Module: %s" % module.__name__,
			"snippet" : s,
			"url" : "http://docs.python.org/library/%s.html" % module.__name__,
			"display_url" : "Show on docs.python.org"
		}
	except ImportError:
		return None

def sha1(query):
	import hashlib
	return {
		"snippet" :  hashlib.sha224(query).hexdigest(),
		"style" : "goodies",
		"title" : "SHA1: %s" % query
	}

def weather(query):
	import engine, config
	if query == "":
		loc = engine.location()
		if not loc:
			return None
		location = "where you are now"
		query = "%s,%s" % (loc[0], loc[1])
	else:
		location = query
	
	j = engine.getJson("http://api.wunderground.com/api/%s/forecast/q/%s.json" % (config.weatherunderground_key, query))
	if 'forecast' in j:
		s = []
		for day in j['forecast']['txt_forecast']['forecastday'][:5]:
			s.append( "<img src='%s' /><br/><strong>%s</strong><br/>%s" % ( day['icon_url'], day['title'], day['fcttext'] ) )
		s = engine.grid(s)	
	
		return {
			"snippet" : s,
			"style" : "goodies",
			"url" : "http://www.wunderground.com/",
			"display_url" : "Powered by WeatherUnderground",
			"title" : "Weather for %s" % location
		}

def revision(query):
	import json, random
	j = json.load(open("asset/revision.json", 'r'))
	if query == "all":
		return {
			"title" : "Revision",
			"snippet" : '<hr/>'.join(j),
			"style" : "goodies"
		}
	else:
		return {
			"title" : "Revision",
			"snippet" : random.choice(j),
			"style" : "goodies"
		}

def life(query):
	if query.lower().startswith("the universe and everything"):
		return {
			"title" : "Life The Universe and Everything",
			"snippet" : "42",
			"style" : "goodies"
		}
def where(query):
	if query.lower().startswith("am i") or query.lower().startswith("me"):
		from engine import location
		loc = location()
		if loc != None:
			return {
				"style" : "goodies",
				"title" : "You are here:",
				"snippet" : "<img src='http://maps.googleapis.com/maps/api/staticmap?center=%s&sensor=false&size=512x250&zoom=14' />" % "%s,%s" % (loc[0], loc[1])
			}

def test(query):
	return {
		"style" : "goodies",
		"title" : "Test",
		"snippet" : "Test OK"
	}

def user(query):
	if query == 'agent':
		import os
		ua = os.environ['HTTP_USER_AGENT']
		return {
			"style" : "goodies",
			"title" : "User Agent: %s" % ua
		}

def website(raw_query):
	results = []
	import urllib
	query = urllib.quote(raw_query)
	# It's a URL
	try:
		j = oembed("http://api.embed.ly/1/oembed?key=9343ff4a0bdc11e1858e4040d3dc5c07&url=%s&maxwidth=500" % raw_query)
		results.append({
			"style" : "embed",
			"title" : "Embed.ly",
			"snippet" : j
		})
	except Exception:
		pass
	results.append({
		"style" : "url",
		"title" : "Go to url",
		"url" : raw_query,
		"display_url" : raw_query
	})
	results.append({
		"style" : "url",
		"title" : "Google Cache of URL",
		"url" : "https://webcache.googleusercontent.com/search?q=cache:%s" % query,
		"display_url" : "Google Cache of %s" % raw_query
	})
	results.append({
		"style" : "url",
		"title" : "Archive.org of URL",
		"url" : "http://wayback.archive.org/web/*/%s" % query,
		"display_url" : "Archive.org of %s" % raw_query
	})
	results.append({
		"style" : "url",
		"title" : "Translate with Google Translate",
		"url" : "http://translate.google.com/translate?u=%s&act=url" % query,
		"display_url" : "Google Translation of %s" % raw_query
	})
	return results

goodies = {
	"binary" : intToBinary,
	"random" : random,
	"python" : pythonLib,
	"define" : dictionary,
	"dictionary" : dictionary,
	"sha1" : sha1,
	"weather" : weather,
	"revision" : revision,
	"life" : life,
	"user" : user,
	"test" : test,
	"where" : where, # Where am I?
	"locate" : where, # Locate me
	"find" : where, # Find me
}
