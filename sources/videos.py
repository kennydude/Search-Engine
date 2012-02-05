from engine import getJson, shorten
import config, magic, urllib, config

def youtube(q_query, raw_query, page):
	config.result_class = ' thumbnails'
	results = []
	s = ((page-1)*12) + 1
	j = getJson('https://gdata.youtube.com/feeds/api/videos?alt=json&q=%s&start-index=%i&max-results=12' % (q_query, s))
	for v in j['feed']['entry']:
		tl = v['media$group']['media$thumbnail']
		for th in tl:
			if th['width'] == 120:
				t = th['url']
		for l in v['link']:
			if l['type'] == 'text/html' and l['rel'] == "alternate":
				u = l['href']
		import urlparse
		url = urlparse.urlparse(u)
		vid = urlparse.parse_qs(url.query)['v'][0]

		results.append({
			"style" : "video",
			"thumbnail" : t,
			"url" : u,
			"source" : "YouTube",
			"user" : v['author'][0]['name']["$t"],
			"title" : v['title']['$t'],
			"player" : '<iframe width="700" height="425" src="http://www.youtube.com/embed/%s?autoplay=1"></iframe>' % vid
		})
	
	return results


