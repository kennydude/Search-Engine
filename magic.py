from engine import *

def youtubeVideo(url, r):
	import urlparse
	u = urlparse.urlparse(url)
	v = urlparse.parse_qs(u.query)['v'][0]
	return {
		"url" : r['Url'],
		"display_url" : r['DisplayUrl'],
		"title" : r['Title'],
		"snippet" : '<iframe width="400" height="225" src="http://www.youtube.com/embed/%s"></iframe>' % v,
		"style" : "magic"
	}

def youtubeUser(url, r):
	up = url.split('/')
	go = False
	for uup in up:
		if go == True:
			u = uup
			go = False
		if uup == "user":
			go = True
	
	j = getJson("https://gdata.youtube.com/feeds/api/users/%s?alt=json" % u)
	s = j['entry']['content']['$t'] + "<br/><table><tr>"

	j = getJson("https://gdata.youtube.com/feeds/api/users/%s/uploads?alt=json&max-results=6" % u)
	for v in j['feed']['entry']:
		tl = v['media$group']['media$thumbnail']
		for th in tl:
			if th['width'] == 120:
				t = th['url']
		s += "<td><a href='%s' title='%s'><img src='%s' /></a></td>" % ( v['media$group']['media$player'][0]['url'], v['title']['$t'], t )
	s += '</tr></table>'
		
	return {
		"url" : r['Url'],
		"display_url" : r['DisplayUrl'],
		"title" : r['Title'],
		"snippet" : s,
		"style" : "magic"
	}

def gsmAreana(url, r):
	s = getBeatifulXML(r['Url'])
	sn = '''
<table>
<tr><td>
%s
</td><td>
%s
</td></tr>
</table>
''' % (s.find("div", id="specs-cp-pic").prettify(), s.find("div", id="specs-list").prettify())

	return {
		"url" : r['Url'],
		"display_url" : r['DisplayUrl'],
		"title" : r['Title'],
		"snippet" : sn,
		"style" : "magic"
	}

def twitter(url, r):
	if url.split('.')[0].split('/')[-1] in ['dev', 'help']:
		return None
	u = url.split('/')[-1]
	j = getJson("http://api.twitter.com/1/users/show.json?id=%s" % u)
	set_debug_info(j)

	s = j['description']  
	if 'status' in j:
		s += "<br/>Latest Tweet:<br/>" + oembed("https://api.twitter.com/1/statuses/oembed.json?id=%s" % j['status']['id_str'])

	return {
		"url" : url,
		"display_url" : r['DisplayUrl'],
		"title" : "%s on Twitter" % u,
		"snippet" : s,
		"style" : "magic"
	}

def tumblr(url, r):
	import json
	if "www.tumblr.com" in url:
		return None
	
	u = urllib2.urlopen('/'.join(url.split('/')[0:3]) + '/api/read/json?callback=1&num=3').read()
	u = u[2:-3]
	j = json.loads(u)

	s = "<table><tr><td>%s</td>" % j['tumblelog']['description']
	for p in j['posts']:
		c = ''
		if p['type'] == "video":
			c = p['video-player-250']
		elif p['type'] == 'regular':
			c = '<div class="window"><strong>%s</strong><br/>%s</div>' % (p['regular-title'], p['regular-body'])
		elif p['type'] == "photo":
			c = '<div class="window"><img src="%s" /><br/>%s</div>' % (p['photo-url-250'], p['photo-caption'])
		elif p['type'] == "answer":
			c = '<div class="window">Q: %s<br/>A: %s</div>' % (p['question'], p['answer'])
		s += "<td>%s</td>" % c
	s += "</tr></table>"

	return {
		"url" : url,
		"display_url" : r['DisplayUrl'],
		"title" : j['tumblelog']['title'],
		"snippet" : s,
		"style" : "magic"
	}

def facebook(url, r):
	u = url.split('/')[-1]
	j = getJson("http://graph.facebook.com/%s" % u)
	set_debug_info(j)
	if not 'picture' in j:
		j['picture'] = 'u.jpg'
	if not 'personal_info' in j:
		if 'gender' in j:
			j['personal_info'] = j['gender']
		elif 'description' in j:
			j['personal_info'] = j['description']
		else:
			j['personal_info'] = ""

	s = '<table><tr><td><img src="%s" /></td><td><strong>%s</strong><br/>%s</td></tr></table>' % (j['picture'], j['name'], j['personal_info'])

	return {
		"url" : url,
		"display_url" : r['DisplayUrl'],
		"title" : r['Title'],
		"snippet" : s,
		"style" : "magic"
	}

def stackExchange(url, r):
	j = getJson("http://api.stackoverflow.com/1.1/questions/%s?answers=true&body=true" % url.split("/")[4])
	q = j['questions'][0]

	s = q['body']
	muv = 0
	mub = ''
	ab = ''
	for a in q['answers']:
		if a['up_vote_count'] > muv:
			mub = a['body']
		if a['accepted'] == True:
			ab = a['body']
	if mub != '':
		s += "<strong>Most upvoted answer:</strong><br/>%s" % mub
	if ab != '':
		s += "<strong>Accepted Answer:</strong><br/>%s" % ab
	
	return {
		"url" : url,
		"display_url" : r['DisplayUrl'],
		"title" : "Q: " + q['title'],
		"snippet" : s,
		"style" : "magic"
	}

magic = {
	"http://www.youtube.com/user/" : youtubeUser,
	"youtube.com/watch?v=" : youtubeVideo,
	"http://www.gsmarena.com/" : gsmAreana,
	"twitter.com" : twitter,
	".tumblr.com" : tumblr,
	"facebook.com" : facebook,
	"stackoverflow.com/questions/" : stackExchange
}
