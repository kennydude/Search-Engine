'''
@kennydude Search Engine
'''
import cgi, json, urllib2, sys, urllib, os.path, hashlib, time
import StringIO

debug_output = True

from mako.template import Template
from mako.lookup import TemplateLookup

def tplate(f, context):
	print get_tplate(f, context)

def location():
	'''
	Gets any location data
	'''
	lat = cgi.FieldStorage().getvalue('lat')
	if not lat:
		print "<script type='text/javascript'>$(document).ready(function(){request_location();});</script>"
	else:
		lon = cgi.FieldStorage().getvalue('long')
		return (lat, lon)
	
def get_tplate(f, context):
	from hashbang import redir_bang, view_bang
	context['hashbang'] = redir_bang
	context['viewbang'] = view_bang
	l = TemplateLookup(directories=['asset/'])
	t = l.get_template('%s.html' % f)
	return t.render_unicode(**context).encode('UTF8')

debug_info = ""
def set_debug_info(v):
	global debug_info
	debug_info = v

def getUrlRequest(url):
	import os
	ua = os.environ['HTTP_USER_AGENT']
	return urllib2.Request(url, headers={
		"User-Agent" : ua
	})

def openUrl(url, fresh=False, default="{}"):
	global nocache
	if fresh == True:
		return urllib2.urlopen(getUrlRequest(url))
	f = "%s.html" % hashlib.sha224(url).hexdigest()	
	if os.path.exists(os.path.join("cache", f)) and nocache == False:
		if os.path.getmtime(os.path.join("cache", f)) > time.time() - (60 * 60 * 1):
			return open(os.path.join("cache", f), "r")
	c = open(os.path.join("cache", f), "w")
	try:
		u = urllib2.urlopen(getUrlRequest(url))
		c.write(u.read())
		u.close()
		c.close()
		if nocache == True:
			return open(os.path.join("cache", f), "r")
		else:
			return openUrl(url)
	except Exception as ex:
		c.seek(0)
		c.write(default)
		c.close()
		o = StringIO()
		o.write(default)
		o.seek(0)
		return o

def getJson(url, fresh=False, default="{}"):
	try:
		return json.load(openUrl(url, fresh, default))
	except Exception:
		print "JSON ERROR FOR URL %s WITH JSON OF '%s'" % (url, openUrl(url, fresh, default).read())
		return json.loads(default)

def getBeatifulXML(url, fresh=False):
	from BeautifulSoup import BeautifulSoup
	return BeautifulSoup(openUrl(url, fresh).read())

def getXML(url, fresh=False):
	import xml.etree.ElementTree as ET
	return ET.parse(openUrl(url, fresh))

def debug(*args):
	global debug_output
	if debug_output == True:
		print "DEBUG: %s<br/>" % args

def shorten(s, l):
	if len(s) - 3 > l:
		return s[0:l] + '...'
	return s

def oembed(url):
	j = getJson(url)
	return j['html']

import urllib2
from gzip import GzipFile
from StringIO import StringIO

class GZipProcessor(urllib2.BaseHandler):
	"""A handler to add gzip capabilities to urllib2 requests
	"""
	def http_request(self, req):
		req.add_header("Accept-Encoding", "gzip")
		return req
	https_request = http_request

	def http_response(self, req, resp):
		if resp.headers.get("content-encoding") == "gzip":
		    gz = GzipFile(
		                fileobj=StringIO(resp.read()),
		                mode="r"
		              )
	#            resp.read = gz.read
	#            resp.readlines = gz.readlines
	#            resp.readline = gz.readline
	#            resp.next = gz.next
		    old_resp = resp
		    resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
		    resp.msg = old_resp.msg
		return resp
	https_response = http_response

opener = urllib2.build_opener(GZipProcessor())
urllib2.install_opener(opener)

query = cgi.FieldStorage().getvalue('q')
page = cgi.FieldStorage().getvalue('page')
nocache = cgi.FieldStorage().getvalue('nocache')
source = cgi.FieldStorage().getvalue('source')

if not page:
	page = 1
else:
	page = int(page)
if not nocache:
	nocache = False
else:
	nocache = True

if not query:
	import widget
	print "Content-Type: text/html; charset=utf-8"
	print ""
	tplate("index", {"widgets" : widget.doWidgets, "raw_query" : ""})
	sys.exit(0)

import config

# Now prepare results

from hashbang import redir_bang, view_bang
results = []

hashbang = None

words = query.split(' ')

raw_query = query
try:
	for word in words:
		if word[0] == "!":
			hashbang = word[1:]
			words.remove(word)
except IndexError:
	pass

query = ' '.join(words)
q_query = urllib.quote(query)

if hashbang is not None:
	hashbang = hashbang.lower()

if hashbang in redir_bang.keys():
	print "Location: %s" % ( redir_bang[hashbang] % query )
	print ""
	sys.exit(0)

view = 'normal'
if hashbang in view_bang.keys():
	view = hashbang

print "Content-Type: text/html; charset=utf-8"
print ''

if not source:
	import sources
	tplate("header", { "search" : query, "raw_query" : raw_query, "view" : view })

	if len(config.search_widgets) != 0:
		import widget
		print '<li class="widgets">'
		print widget.doWidgets(config.search_widgets)
		print '</li>'

	extra = ''
	
	l = location()
	if l != None:
		extra += '&lat=%s&long=%s' % (l[0], l[1])
	
	if view != 'normal':
		sources.sources = view_bang[view] + sources.sources
	
	tplate("footer", { "search" : query, "query" : raw_query, "nextpage" : page + 1, "page" : page, "sources" : sources.sources, "extra" : extra, "view" : view })
else:
	import goodies, magic, sources
	# Here we go...
	if source is not None:
		config.result_class = ''
		config.pre_output = ''

		results = getattr(sources, source)(q_query, raw_query, page)
		result_class = config.result_class

		print config.pre_output
		print '<ul class="results%s">' % result_class
		for result in results:
			if "style" in result and os.path.exists("asset/result_%s.html" % result['style']):
				tplate("result_%s" % result['style'], result)
			else:
				tplate("result", result)
		print '</ul>'
# TODO: Forward images into this

'''
if hashbang == 'images':
	# Images!: D
	j = getJson("https://api.instagram.com/v1/tags/%s/media/recent?client_id=%s" % ( q_query, config.instagram_key ), default='{ "data" : [] }' )
	if len(j['data']) != 0:
		result = {
			"source" : "Instagram",
			"images" : [],
			"style" : "image"
		}
		for r in j['data']:
			result['images'].append({
				"url" : r['link'],
				"display_url" : r['link'],
				"title" : shorten(r['caption']['text'], 140),
				"user" : r['user']['username'],
				"image" : r['images']['low_resolution']['url'],
			})
		results.append(result)
	j = getJson("http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&text=%s&format=json&nojsoncallback=1&per_page=20" % (config.flickr_key, q_query), default='{ "photos" : { "photo" : [] } }' )
	if len(j['photos']['photo']) != 0:
		result = {
			"source" : "Flickr",
			"images" : [],
			"style" : "image"
		}
		for r in j['photos']['photo']:
			result['images'].append({
				"url" : "http://flickr.com/photos/%s/%s" % (r['owner'], r['id']),
				"display_url" : "http://flic.kr/%s" % base58(int(r['id'])),
				"title" : shorten(r['title'], 140),
				"user" : r['owner'],
				"image" : "http://farm%s.static.flickr.com/%s/%s_%s_t.jpg" % (r['farm'], r['server'], r['id'], r['secret']),
			})
		results.append(result)


# Generic Searches


# Whoosh


def add_normal(r):
	global results
	results.append({
		"url" : r['Url'],
		"display_url" : r['DisplayUrl'],
		"title" : r['Title'],
		"snippet" : r['Description'],
		"style" : "bing"
	})


if len(words) == 1 and raw_query.startswith("http"):
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
		"url" : "https://webcache.googleusercontent.com/search?q=cache:%s" % raw_query,
		"display_url" : "Google Cache of %s" % raw_query
	})
	results.append({
		"style" : "url",
		"title" : "Archive.org of URL",
		"url" : "http://wayback.archive.org/web/*/%s" % raw_query,
		"display_url" : "Archive.org of %s" % raw_query
	})






	''
	if result['style'] == 'image':
		i = ''
		for image in result['images']:
			i = i + iit.safe_substitute(image)
		print it.safe_substitute({ "images" : i, "source" : result['source'] }).encode('UTF8')
	else:
		print t.safe_substitute(**result).encode('UTF8')
	''

if len(results) == 0:
	print "NO RESULTS ;__;"


'''
