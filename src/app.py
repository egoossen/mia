import test_import, miaprinter, dotenv, os, canvasimport, webbrowser
import ekgconfig as cfg
import course as crs

class App(object):
	def __init__(self, importer, printer):
		self.canvas = importer
		self.printer = printer
		try:
			self.cfg = cfg.load('config.json')
		except FileNotFoundError:
			self.cfg = dict()
			self.import_courses()
	
	def import_courses(self):
		self.cfg['courses'] = self.canvas.import_courses()
		cfg.save(self.cfg, 'config.json')
	
	def get_data(self, course_id):
		course_name = self.cfg['courses'][course_id]
		self.course = crs.Course(
			course_id = course_id,
			course_name = course_name,
			importer = self.canvas,
			printer = self.printer
		)
		return self.course.get_data()

	def print_report(self, all_data):
		self.course.update_data(all_data)
		report_data = {}
		remove_students = {student_id for student_id in all_data['students']}
		for student_id, student_name in all_data['students'].items():
			report_data[student_name] = list()
			for assignment_id, assignment in all_data['assignments'].items():
				if all_data['missing'][student_id][assignment_id]:
					report_data[student_name].append(assignment)
					remove_students.discard(student_id)
		for student_id in remove_students:
			del report_data[all_data['students'][student_id]]

		html_file = self.printer.dict2html(self.course.get_name(), report_data)
		outfile = self.course.get_name().lower().replace(' ','-') + '-mia-report.html'
		with open(outfile, 'w') as f:
			f.write(html_file)
		webbrowser.open(outfile)
	

if __name__ == '__main__':
	#dotenv.load_dotenv()
	#URL = os.getenv('CANVAS_API_URL')
	#KEY = os.getenv('CANVAS_API_KEY')
	printer = miaprinter.MiaPrinter()
	#importer = canvasimport.CanvasImporter(URL, KEY)
	importer = test_import.TestImporter()
	app = App(importer = importer,printer = printer)


