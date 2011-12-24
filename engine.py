'''
@kennydude Search Engine
'''
import cgi, json, urllib2, sys, urllib, os.path, hashlib, time
from string import Template

redir_bang = {
	"ddg" : "http://ddg.gg?q=%s",
	"google" : "http://google.com/search?q=%s",
	"bing" : "http://bing.com?q=%s",
	"yahoo" : "http://yahoo.com/search?p=%s",
	"minewiki" : "http://www.minecraftwiki.net/Special:Search?search=%s",
	"minecraftwiki" : "http://www.minecraftwiki.net/Special:Search?search=%s",
	"minecraftforum" : "http://www.minecraftforum.net/index.php?app=core&module=search&do=search&search_term=%s",
	"xda" : "http://www.google.com/cse?q=%s&cx=partner-pub-2900107662879704%%3Afs7umqefhnf",
	"modaco" : "http://android.modaco.com/index.php?app=core&module=search&do=search&search_term=%s",
	"youtube" : "http://youtube.com/results?search_query=%s",
	"wolfram" : "http://wolframalpha.com/input?i=%s",
	"android" : "http://developer.android.com/search.html#q=%s&t=0",
	"github" : "https://github.com/search?q=%s&type=Everything&repo=&langOverride=&start_value=1",
	"market" : "https://market.android.com/search?q=%s&c=apps"
}

debug_output = True
pre_output = open("asset/header.html", 'r').read()
result_output = u'''
<li class="result $style">
	<div>
		<strong>$title</strong><br/>
		$snippet<br/>
		<a href="$url">$display_url</a>
	</div>
</li>
'''

image_result_output = u'''
<li class="result image">
	<div>
		<table><tr>$images</tr></table>
		via $source
	</div>
</li>
'''

image_in_result_output = u'''
<td>
<a href="$url">
<img src="$image" class='scaled' /></a><br/>
<div class="caption"><strong>$title</strong></div>by $user
<a href="$url">$display_url</a>
</td>
'''

end_output = u'''
<li>
<a href="?q=%(query)s&page=%(nextpage)s">More</a>
</li>
</ul>
</div></div>
<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$("img.scaled").load(function(){
		var img = $(this), width = img.width(), height = img.height();
		img.css("max-width", "1000px !important");
		if(width == height) {
			img.width(200).height(200);
		} else if(width > height) {
			img.height(Math.round(height / width * 200)).width(200);
		} else {
			img.width(Math.round(width / height * 200)).height(200);
		}
	});
});
</script>
</body>
</html>
'''

debug_info = ""
def set_debug_info(v):
	global debug_info
	debug_info = v

def openUrl(url, fresh=False):
	if fresh == True:
		return urllib2.urlopen(url)
	f = "%s.html" % hashlib.sha224(url).hexdigest()	
	if os.path.exists(os.path.join("cache", f)):
		if os.path.getmtime(os.path.join("cache", f)) > time.time() - (60 * 60 * 1):
			return open(os.path.join("cache", f), "r")
	c = open(os.path.join("cache", f), "w")
	u = urllib2.urlopen(url)
	c.write(u.read())
	u.close()
	c.close()
	return openUrl(url)

def getJson(url, fresh=False):
	return json.load(openUrl(url, fresh))

def getBeatifulXML(url, fresh=False):
	from BeautifulSoup import BeautifulSoup
	return BeautifulSoup(openUrl(url, fresh).read())

def getXML(url, fresh=False):
	import xml.etree.ElementTree as ET
	return ET.parse(openUrl(url, fresh))

__b58chars = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
__b58base = len(__b58chars) # let's not bother hard-coding

def base58(value):
    """
    encode integer 'value' as a base58 string; returns string
    """

    encoded = ''
    while value >= __b58base:
        div, mod = divmod(value, __b58base)
        encoded = __b58chars[mod] + encoded # add to left
        value = div
    encoded = __b58chars[value] + encoded # most significant remainder
    return encoded

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
if not page:
	page = 0
else:
	page = int(page)

if not query:
	print "Content-Type: text/html; charset=utf-8"
	print ""
	print open('asset/index.html', 'r').read()
	sys.exit(0)

import config, goodies, magic

# Now prepare results
results = []

hashbang = None

words = query.split(' ')

if words[0] in goodies.goodies.keys():
	try:
		s = goodies.goodies[words[0]](' '.join(words[1:]))
		if s != None:
			results.append(s)
	except Exception as ex:
		results.append({
			"style" : "error",
			"title" : "An error occured: %s" % str(ex)
		})

raw_query = query
for word in words:
	if word[0] == "!":
		hashbang = word[1:]
		words.remove(word)

query = ' '.join(words)
q_query = urllib.quote(query)

if hashbang is not None:
	hashbang = hashbang.lower()

if hashbang in redir_bang.keys():
	print "Location: %s" % ( redir_bang[hashbang] % query )
	print ""
	sys.exit(0)

print "Content-Type: text/html; charset=utf-8"
print ''

if hashbang == 'images':
	# Images!: D
	j = getJson("https://api.instagram.com/v1/tags/%s/media/recent?client_id=%s" % ( q_query, config.instagram_key ) )
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
	j = getJson("http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&text=%s&format=json&nojsoncallback=1&per_page=20" % (config.flickr_key, q_query) )
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
j = getJson("http://localhost/wiki/search.php?q=%s" % q_query)
for r in j:
	results.append({
		"url" : u"http://localhost/wiki/doku.php?id=%s" % urllib.quote(r['id']),
		"display_url" : "LocalWiki://%s" % r['id'],
		"snippet" : r['snip'],
		"title" : unicode(r['title']),
		"style" : u"special"
	})

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

j = getJson("http://api.bing.net/json.aspx?sources=Web+RelatedSearch&AppId=%s&query=%s&Web.Count=10&Web.Offset=%s" % (config.bing_api_key, q_query, page * 10) )

if 'Results' in j['SearchResponse']['Web']:
	for r in j['SearchResponse']['Web']['Results']:
		if 'Description' not in r:
			r['Description'] = ''
		go_magic = False
		for m in magic.magic.keys():
			if m in r['Url']:
				go_magic = magic.magic[m]
		if go_magic != False:
			try:
				set_debug_info("")
				x = go_magic(r['Url'], r)
				if x is not None:
					results.append(x)
				else:
					add_normal(r)
			except Exception as ex:
				import traceback
				results.append({
					"style" : "error",
					"title" : "An error occured: %s" % repr(ex) + "<br/>" + traceback.format_exc().replace("\n", "<br/>"),
					"url" : r['Url'],
					"snippet" : "<pre>%s</pre>" % debug_info
				})
				add_normal(r)
		else:
			add_normal(r)

if 'RelatedSearch' in j['SearchResponse']:
	s = "<ul>"
	for r in j['SearchResponse']['RelatedSearch']['Results']:
		s += "<li><a href='?q=%s'>%s</a></li>" % (urllib.quote(r['Title'].encode("utf8")), r['Title'])
	s += "</ul>"
	results.append({
		"style" : "related_search bing",
		"title" : "Releated Searches",
		"snippet" : s
	})

print pre_output % { "search" : query, "raw_query" : raw_query }

t = Template(result_output)
it = Template(image_result_output)
iit = Template(image_in_result_output)

for result in results:
	if result['style'] == 'image':
		i = ''
		for image in result['images']:
			i = i + iit.safe_substitute(image)
		print it.safe_substitute({ "images" : i, "source" : result['source'] }).encode('UTF8')
	else:
		print t.safe_substitute(**result).encode('UTF8')

if len(results) == 0:
	print "NO RESULTS ;__;"

print end_output % { "query" : raw_query, "nextpage" : page + 1}
