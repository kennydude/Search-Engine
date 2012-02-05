from engine import getJson, shorten
import config, magic, urllib, config

header = '''
<h2>
<button class='btn hider'>
<i class="icon-chevron-down"></i>
</button>
Results from %s</h2>
'''

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

def instagram(q_query, raw_query, page):
	results = []
	config.pre_output = header % "Instagram"
	config.result_class = ' thumbnails'
	j = getJson("https://api.instagram.com/v1/tags/%s/media/recent?client_id=%s" % ( q_query, config.instagram_key ), default='{ "data" : [] }' )
	if len(j['data']) != 0:
		for r in j['data']:
			results.append({
				"url" : r['link'],
				"style" : "image",
				"source" : "Instagram",
				"display_url" : r['link'],
				"title" : shorten(r['caption']['text'], 140),
				"user" : r['user']['username'],
				"image" : r['images']['low_resolution']['url'],
			})
	return results

def flickr(q_query, raw_query, page):
	results = []
	config.pre_output = header % "Flickr"
	config.result_class = ' thumbnails'
	j = getJson("http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&text=%s&format=json&nojsoncallback=1&per_page=20" % (config.flickr_key, q_query), default='{ "photos" : { "photo" : [] } }' )
	if len(j['photos']['photo']) != 0:
		for r in j['photos']['photo']:
			results.append({
				"url" : "http://flickr.com/photos/%s/%s" % (r['owner'], r['id']),
				"display_url" : "http://flic.kr/%s" % base58(int(r['id'])),
				"title" : shorten(r['title'], 140),
				"user" : r['owner'],
				"style" : "image",
				"source" : "flickr",
				"image" : "http://farm%s.static.flickr.com/%s/%s_%s_t.jpg" % (r['farm'], r['server'], r['id'], r['secret']),
			})
	return results
