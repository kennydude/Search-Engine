from engine import getJson
import config, magic, urllib

def add_normal(r, results):
	results.append({
		"url" : r['Url'],
		"display_url" : r['DisplayUrl'],
		"title" : r['Title'],
		"snippet" : r['Description'],
		"style" : "bing"
	})

debug_info = ""
def set_debug_info(v):
	global debug_info
	debug_info = v

def bing(q_query, raw_query, page):
	results = []
	import magic
	j = getJson("http://api.bing.net/json.aspx?sources=Web+RelatedSearch&AppId=%s&query=%s&Web.Count=10&Web.Offset=%s" % (config.bing_api_key, q_query, (page-1) * 10), default='{ "SearchResponse" : { "Web" : { } } }' )

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
						x["style"] += " bing"
						results.append(x)
					else:
						add_normal(r, results)
				except Exception as ex:
					import traceback
					results.append({
						"style" : "error",
						"title" : "An error occured: %s" % repr(ex) + "<br/>" + traceback.format_exc().replace("\n", "<br/>"),
						"url" : r['Url'],
						"snippet" : "<pre>%s</pre>" % debug_info
					})
					add_normal(r, results)
			else:
				add_normal(r, results)
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
	return results

def whoosh(q_query, raw_query, page):
	results = []
	try:
		import internal_search
		with internal_search.ix.searcher() as searcher:
			from whoosh.qparser import QueryParser
			parser = QueryParser("keywords", internal_search.ix.schema)
			myquery = parser.parse('"%s"' %raw_query)
			w_results = searcher.search(myquery)
			for r in w_results:
				s = ''
				if 'official' in r:
					s = ' official'
				results.append({
					"style" : "internal_search%s" % s,
					"title" : r['title'],
					"url" : r['link'],
					"snippet" : r['content'],
					"display_url" :  r['link']
				})
	except Exception as ex:
		import traceback
		results.append({
			"style" : "error",
			"title" : "An error occured: %s" % repr(ex) + "<br/>" + traceback.format_exc().replace("\n", "<br/>"),
			"snippet" : "<pre>%s</pre>" % debug_info
		})
	return results

def localwiki(q_query, raw_query, page):
	results = []
	try:
		j = getJson("http://localhost/wiki/search.php?q=%s" % q_query, True)
	except Exception:
		return {}
	for r in j:
		results.append({
			"url" : u"http://localhost/wiki/doku.php?id=%s" % urllib.quote(r['id']),
			"display_url" : "LocalWiki://%s" % r['id'],
			"snippet" : r['snip'],
			"title" : unicode(r['title']),
			"style" : u"special"
		})
	return results

def ddg(q_query, raw_query, page):
	results = []
	j = getJson("http://api.duckduckgo.com/?q=%s&format=json" % q_query)
	if j['Abstract'] != '':
		results.append({
			"url" : j["AbstractURL"],
			"title" : j["Heading"],
			"style" : "duckduckgo magic",
			"display_url" : "Source: %s (via DDG)" % j['AbstractSource'],
			"snippet" : j["Abstract"]
		})
	if j['Definition'] != '':
		results.append({
			"url" : j['DefinitionURL'],
			"snippet" : j['Definition'],
			"style" : "duckduckgo magic",
			"display_url" : "Source: %s (via DDG)" % j['DefinitionSource']
		})
	if j['Answer'] != '':
		results.append({
			"style" : "duckduckgo magic",
			"display_url" : "%s on DuckDuckGo" % j['AnswerType'],
			"url" : "http://ddg.gg?q=%s" % q_query,
			"snippet" : j['Answer']
		})
	for r in j['Results']:
		results.append({
			"style" : "duckduckgo",
			"url" : r['FirstURL'],
			"snippet" : r['Text'],
			"title" : r['Result']
		})
	s = '<ul>'
	for r in j['RelatedTopics']:
		if 'Result' in r:
			s += '<li>%s</li>' % r['Result']
	if s != '<ul>':
		results.append({
			"style" : "duckduckgo related",
			"snippet" : s,
			"title" : "DuckDuckGo Related Topics"
		})
	return results

def goodies(q_query, raw_query, page):
	results = []
	words = raw_query.split(' ')
	import goodies
	if words[0].lower() in goodies.goodies.keys():
		try:
			s = goodies.goodies[words[0].lower()](' '.join(words[1:]))
			if s != None:
				results.append(s)
		except Exception as ex:
			results.append({
				"style" : "error",
				"title" : "An error occured: %s" % str(ex)
			})
	return results
