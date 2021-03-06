'''
@kennydude Search Engine
'''
import cgi, json, urllib2, sys, urllib, os.path, hashlib, time
import StringIO

debug_output = True

from mako.template import Template
from mako.lookup import TemplateLookup

def join_bxml(x):
	o = ''
	for i in x:
		o += i.string
	return o

def tplate(f, context):
	print get_tplate(f, context)

def location(output = True):
	'''
	Gets any location data
	'''
	lat = cgi.FieldStorage().getvalue('lat')
	if not lat:
		if output:
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

def grid(items, width=2):
	o = '<div class="row">'
	for i in items:
		o += '<div class="span%i">%s</div>' % (width, i)
	o += '</div>'
	return o

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
elif query == 'opensearch:plugin':
	print "Content-Type: text/xml; charset=utf-8"
	print ""
	import os
	url = 'http://' + os.environ['SERVER_NAME'] + os.environ['REQUEST_URI'].replace('opensearch%3Aplugin', '{searchTerms}')
	iurl = url.replace('search.cgi?q={searchTerms}', 'asset/favicon.png')
	print '''<?xml version="1.0" encoding="UTF-8"?>  
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/"> 
	<ShortName>Search</ShortName>  
	<Description>Search</Description>  
	<InputEncoding>UTF8</InputEncoding>  
	<Image width="24" height="24" type="image/png">%s</Image>  
	<Url type="text/html" method="get" template="%s" />
</OpenSearchDescription>  
''' % (iurl, url)
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
	if type(redir_bang[hashbang]) == tuple:
		if len(words) == 0:
			print "Location: %s" % redir_bang[hashbang][0]
		else:
			print "Location: %s" % ( redir_bang[hashbang][1] % query )
	else:
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
	
	l = location(False)
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

