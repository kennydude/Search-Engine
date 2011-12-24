Search Engine by @kennydude
===========================

Setup
-----

Just pop in your Apache Website.

A few notes:
* You need a config.py with your details, as my API keys are mine
* CGI needs enabling
* I have a DokuWiki set up at http://localhost/wiki/ which you will need the search.php file from the doku folder

Config.py
---------

	# Config

	bing_api_key = "key"
	instagram_key = "key"
	flickr_key = "key"

	dictionary_com_key = "key"
	embedy_ly_key="key"

	default_weather = "Your location"
	weatherunderground_key = "key"

How it's built
--------------

We have engine.py which contains the bulk of everything, but there is goodies.py which provide some nice goodies like "random word" or "sha1 text" and there is magic.py which allows us to do some nice magic with urls. This includes if we see a twitter link it'll get turned into a box with all the twitter data! :D
