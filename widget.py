# Widgets for Search Front Page

def revisionWidget(c):
	import json, random
	j = json.load(open("asset/revision.json", 'r'))
	return "<strong>Revision Byte:</strong><br/>%s" % random.choice(j)

def websiteSnippetWidget(c):
	import engine
	j = engine.getBeatifulXML(c[0])
	if len(c) == 3:
		w = c[2]
	else:
		w = "%s"
	x = ''
	for i in c[1]:
		x += j.findAll(**i)[0].prettify()
	return w % x

widgets = {
	"revision" : revisionWidget,
	"websiteSnippet" : websiteSnippetWidget
}

def doWidgets(c = None):
	if c == None:
		import config
		c = config.widgets
	o = ''
	for widget in c:
		wc = None
		if type(widget) == tuple:
			wc = widget[1:]
			widget = widget[0]
		try:
			o += '<div class="widget">%s</div>' % widgets[widget](wc)
		except Exception as ex:
			o += '<div class="widget">An error occured during rendering widget %s:<br/>%s</div>' % (widget, repr(ex))
	return o
