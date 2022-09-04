import jinja2, sys #pdfkit, sys

class MiaPrinter(object):
	def __init__(self):
		pass

	def dict2html(self, course_name, data):
		myheaders = ['Student Name', 'Assignment Name', 'Points Possible', 'Due Date']
		#if getattr(sys, 'frozen', False):
		#	bundle_dir = sys._MEIPASS
		#	loader = jinja2.FileSystemLoader(bundle_dir)
		#else:
		loader = jinja2.FileSystemLoader('./')
		subs = jinja2.Environment(
			loader = loader,
			trim_blocks = True,
			lstrip_blocks = True,
		).get_template('template.html').render(
			title = course_name,
			myheaders = myheaders,
			mydata = data
		)
		return subs

	# Methods below this line are deprecated
	def html2pdf(self, html, outfile):
		options = {
			'page-size': 'Letter',
			'margin-top': '0.75in',
			'margin-right': '0.75in',
			'margin-bottom': '0.75in',
			'margin-left': '0.75in',
			'encoding': 'utf-8',
			'user-style-sheet': 'style1.css'
		}
		#pdfkit.from_string(html, outfile, options=options)

	def dict2pdf(self, course_name, data, outfile):
		html_str = self.dict2html(course_name, data)
		self.html2pdf(html_str, outfile)
