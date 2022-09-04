#import miaprinter, test_import, canvasimport, dotenv, os
import ekgconfig as cfg, time
from collections import OrderedDict

class Course(object):
	def __init__(self,course_id,course_name,printer,importer):
		self.id = course_id
		self.name = course_name
		self.printer = printer
		self.canvas = importer
		self.data_file = self.name.lower().replace(' ','-') + '-data.json'

		self.data = {'assignments':dict(),'students':dict(),'missing':dict()}
		try:
			self.data = cfg.load(config_file = self.data_file)
		except FileNotFoundError:
			self.data['students'] = self.canvas.import_students(self.id)
			for student_id in self.data['students']:
				if not student_id in self.data['missing']:
					self.data['missing'][student_id] = dict()

			self.add_assignments(self.get_new_assignments())

	def get_missing(self,assignment_id):
		submission_dict = self.canvas.import_submissions(self.id, assignment_id)
		for student_id in submission_dict:
			self.data['missing'][student_id][assignment_id] = submission_dict[student_id]

	def get_data(self):
		return self.data
	
	def get_name(self):
		return self.name
	
	def update_data(self, data):
		cfg.save(self.data, config_file = self.data_file)

	def get_new_assignments(self):
		assignments = self.canvas.import_assignments(self.id)
		self.new_assignments = dict()
		for key in assignments:
			if key not in self.data['assignments']:
				due_date = time.strptime(assignments[key]['due'],'%Y-%m-%dT%H:%M:%SZ')
				if due_date <= time.localtime():
					assignments[key]['due'] = due_date
					self.new_assignments[key] = assignments[key]
		return self.new_assignments
	
	def add_assignments(self, include_assignments='All'):
		if include_assignments == 'All':
			for assignment_id in self.new_assignments:
				include_assignments[assignment_id] = True
		for assignment_id, assignment in self.new_assignments.items():
			if include_assignments[assignment_id]:
				self.data['assignments'][assignment_id] = assignment
		
		for assignment_id in self.data['assignments']:
			self.get_missing(assignment_id)
		
		cfg.save(self.data, config_file = self.data_file)

if __name__ == '__main__':
	dotenv.load_dotenv()
	URL = os.getenv('CANVAS_API_URL')
	KEY = os.getenv('CANVAS_API_KEY')
	COURSE_ID = 805953
	COURSE_NAME = 'Monster Recognition'
	printer = miaprinter.MiaPrinter()
	#importer = test_import.TestImporter()
	importer = canvasimport.CanvasImporter(URL, KEY)
	course = Course(COURSE_ID, COURSE_NAME,printer,importer)
	data = course.preview()
	course.print_report(data)