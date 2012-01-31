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
	
	widgets = []
	search_widgets = []

Widgets
-------

New! Widgets are small blocks of stuff which do some magical things.

Currently we have

* revision - Enable this and create "asset/revision.json" with a JSON array of strings and one will be shown randomly. This was made by @kennydude in order to revise for exams all of the time! :D

How it's built
--------------

We have engine.py which contains the bulk of everything, but there is goodies.py which provide some nice goodies like "random word" or "sha1 text" and there is magic.py which allows us to do some nice magic with urls. This includes if we see a twitter link it'll get turned into a box with all the twitter data! :D
