import test_import, miaprinter, dotenv, os, canvasimport, webbrowser, time
import ekgconfig as cfg
import course as crs
from collections import OrderedDict

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
	
	def initialize_course(self, course_id):
		course_name = self.cfg['courses'][course_id]
		self.course = crs.Course(
			course_id = course_id,
			course_name = course_name,
			importer = self.canvas,
			printer = self.printer
		)
		new_assignments = self.course.get_new_assignments()
		return new_assignments
	
	def add_assignments(self, include_assignments):
		self.course.add_assignments(include_assignments)

	def get_data(self):
		data = self.course.get_data()
		data['assignments'] = sort_assignments(data['assignments'])
		data['students'] = sort_students(data['students'])
		return data

	def print_report(self, all_data):
		self.course.update_data(all_data)
		report_data = {}
		for assignment_id, assignment in all_data['assignments'].items():
			print(assignment['due'])
			assignment['due'] = time.strftime('%d %b %Y',tuple(assignment['due']))
		remove_students = {student_id for student_id in all_data['students']}
		for student_id, student_name in all_data['students'].items():
			report_data[student_name] = list()
			for assignment_id, assignment in all_data['assignments'].items():
				if all_data['missing'][student_id][assignment_id]:
					#formated_assignment = assignment
					#formated_assignment['due'] = time.strftime('%d %b %Y',assignment['due'])
					report_data[student_name].append(assignment)
					remove_students.discard(student_id)
		for student_id in remove_students:
			del report_data[all_data['students'][student_id]]

		html_file = self.printer.dict2html(self.course.get_name(), report_data)
		outfile = self.course.get_name().lower().replace(' ','-') + '-mia-report.html'
		with open(outfile, 'w') as f:
			f.write(html_file)
		webbrowser.open(outfile)

def sort_students(my_dict):
	student_list = [(key,value) for key,value in my_dict.items()]
	student_list = sorted(student_list,key=return_name)
	sorted_dict = OrderedDict(student_list)
	return sorted_dict

def sort_assignments(my_dict):
	assignment_list = []
	for key,value in my_dict.items():
		assignment_list.append((key,value))
	assignment_list = sorted(assignment_list,key=return_due)
	sorted_dict = OrderedDict(assignment_list)
	return sorted_dict

def return_due(assignment):
	return time.strftime('%Y%m%d',tuple(assignment[1]['due']))

def return_name(student):
	return student[1]

if __name__ == '__main__':
	#dotenv.load_dotenv()
	#URL = os.getenv('CANVAS_API_URL')
	#KEY = os.getenv('CANVAS_API_KEY')
	printer = miaprinter.MiaPrinter()
	#importer = canvasimport.CanvasImporter(URL, KEY)
	importer = test_import.TestImporter()
	app = App(importer = importer,printer = printer)


