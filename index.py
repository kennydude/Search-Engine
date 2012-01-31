'''
Create internal index
'''

import glob
import internal_search as search

print "> Indexing..."

writer = search.ix.writer()

for f in glob.glob("index/*.txt"):
	s = open(f, "r").read().split(u"\n")
	c = {}
	for l in s:
		if l != '':
			l = l.split(u"=", 1)
			c[l[0]] = l[1]
	writer.add_document(**c)
	print "> Indexing %s..." % c['title']

writer.commit()

print "> Done :)"
