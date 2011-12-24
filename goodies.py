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
		return {
			"style" : "goodies",
			"title" : "Python Module: %s" % module.__name__,
			"snippet" : module.__doc__.replace("\n", "<br/>"),
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
		query = config.default_weather
	
	j = engine.getJson("http://api.wunderground.com/api/%s/forecast/q/%s.json" % (config.weatherunderground_key, query))
	if 'forecast' in j:
		s = "<table><tr>"
		for day in j['forecast']['txt_forecast']['forecastday']:
			s += "<td><img src='%s' /><br/><strong>%s</strong><br/>%s</td>" % ( day['icon_url'], day['title'], day['fcttext'] )
		s += "</tr></table>"	
	
		return {
			"snippet" : s,
			"style" : "goodies",
			"url" : "http://www.wunderground.com/",
			"display_url" : "Powered by WeatherUnderground",
			"title" : "Weather for %s" % query
		}

goodies = {
	"binary" : intToBinary,
	"random" : random,
	"python" : pythonLib,
	"define" : dictionary,
	"dictionary" : dictionary,
	"sha1" : sha1,
	"weather" : weather
}
