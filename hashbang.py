import os
ua = os.environ['HTTP_USER_AGENT'].lower()
if 'firefox' in ua:
	addons = 'https://addons.mozilla.org/en-US/firefox/search/?q=%s'

'''
Information:
	"ddg" == becomes ==> !ddg
	Value can be string with %s for direct search-only
	Tuple for shortcut availability
		[0] = Direct no other words
		[1] = Search
'''

redir_bang = {
	# Search Engines: 
	"ddg" : "http://ddg.gg?q=%s",
	"google" : "http://google.com/search?q=%s",
	"bing" : "http://bing.com?q=%s",
	"yahoo" : "http://yahoo.com/search?p=%s",

	# Forus
	"minewiki" : "http://www.minecraftwiki.net/Special:Search?search=%s",
	"minecraftwiki" : "http://www.minecraftwiki.net/Special:Search?search=%s",
	"minecraftforum" : "http://www.minecraftforum.net/index.php?app=core&module=search&do=search&search_term=%s",
	"xda" : "http://www.google.com/cse?q=%s&cx=partner-pub-2900107662879704%%3Afs7umqefhnf",
	"modaco" : "http://android.modaco.com/index.php?app=core&module=search&do=search&search_term=%s",

	# Other sites
	"youtube" : "http://youtube.com/results?search_query=%s",
	"wolfram" : "http://wolframalpha.com/input?i=%s",
	"android" : "http://developer.android.com/search.html#q=%s&t=0",
	"github" : "https://github.com/search?q=%s&type=Everything&repo=&langOverride=&start_value=1",
	"market" : "https://market.android.com/search?q=%s&c=apps",
	"tumblr" : ( "http://tumblr.com", "http://tumblr.com/tagged/%s" ),
	"launchpad" : "https://launchpad.net/+search?field.text=%s",
	"vimeo" : ("http://vimeo.com", "http://vimeo.com/videos?search=%s"),
	"icons" : "http://www.iconfinder.com/search/?q=%s",
	"gmail" : ( "http://gmail.com", "http://mail.google.com/mail/#search/%s" ),
	"translate" : ("http://translate.google.com", "http://translate.google.com/#auto|en|%s" ),

	# Reference
	"wikipedia" : "http://en.wikipedia.org/wiki/Special:Search?search=%s",
	"psychwiki" : "http://www.psychwiki.com/wiki/Special:Search?search=%s",
	"psychology" : "http://psychology.wikia.com/wiki/Special:Search?search=%s",
	"jquery" : "http://api.jquery.com/%s",
	"php" : "http://php.net/manual-lookup.php?pattern=%s&scope=quickref",
	"amazon" : "http://www.amazon.co.uk/s/?url=search-alias%3Daps&field-keywords=%s",

	# Images
	"googleimages" : "https://encrypted.google.com/search?tbm=isch&q=%s",
	"bingimages" : "http://www.bing.com/images/search?q=%s"
}
if addons is not None:
	redir_bang['addons'] = addons

# Now here is the view hashbang
view_bang = {
	"images" : ['flickr', 'instagram'],
	"videos" : ['youtube']
}
