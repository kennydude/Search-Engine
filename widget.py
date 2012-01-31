# Widgets for Search Front Page

def revisionWidget():
	import json, random
	j = json.load(open("asset/revision.json", 'r'))
	return "<strong>Revision Byte:</strong><br/>%s" % random.choice(j)

widgets = {
	"revision" : revisionWidget
}

def doWidgets(c = None):
	if c == None:
		import config
		c = config.widgets
	o = ''
	for widget in c:
		try:
			o += '<div class="widget">%s</div>' % widgets[widget]()
		except Exception as ex:
			o += '<div class="widget">An error occured during rendering widget %s:<br/>%s</div>' % (widget, repr(ex))
	return o
