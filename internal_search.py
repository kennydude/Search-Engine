from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os

schema = Schema(title=TEXT(stored=True),
		link=TEXT(stored=True),
		official=BOOLEAN(stored=True),
		content=TEXT(stored=True),
		twitter=TEXT(stored=True),
		keywords=KEYWORD(stored=True,commas=True, lowercase=True)
	)

if 'REQUEST_METHOD' in os.environ:
	ix = open_dir(os.path.join("cache", "index"))
else:
	ix = create_in(os.path.join("cache", "index"), schema)
