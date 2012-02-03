'''
Create internal index
'''

import glob, os.path, os, time
import internal_search as search

print ">> @kennydude Search Backend update script"
print ">> Updates the backend. We're going to do that now"
print "> Indexing..."

writer = search.ix.writer()

i = 0
for f in glob.glob("index/*.txt"):
	s = open(f, "r").read().split(u"\n")
	c = {}
	for l in s:
		if l != '':
			l = l.split(u"=", 1)
			c[l[0]] = l[1]
	writer.add_document(**c)
	i = i + 1

writer.commit()

print "> Done. %i items indexed :)" % i
print "> Cleaning cache"

i = 0
for f in glob.glob("cache/*.html"):
	if os.path.getmtime(f) > time.time() - (60 * 60 * 1):
		os.remove(f)
		i += 1

print "> Done. %i files cleared" % i
