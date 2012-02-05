'''
Template

def source(q_query, raw_query, page):
	return []
'''
import cgi
source = cgi.FieldStorage().getvalue('source')

if not source:
	sources = [
		'goodies', 'whoosh', 'ddg', 'localwiki', 'bing'
	]
else:
	from sources.web import *
	from sources.images import *
	from sources.videos import *

	sources = [
		goodies, whoosh, ddg, localwiki, bing
	]
