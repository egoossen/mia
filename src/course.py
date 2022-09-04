import random, miaprinter, webbrowser, test_import, canvasimport, dotenv, os
import ekgconfig as cfg

class Course(object):
	def __init__(self,course_id,course_name,printer,importer):
		self.id = course_id
		self.name = course_name
		self.printer = printer
		self.canvas = importer
		self.data_file = self.name.lower().replace(' ','-') + '-data.json'

		self.data = dict()
		try:
			self.data = cfg.load(config_file = self.data_file)
		except FileNotFoundError:
			self.data['assignments'] = self.canvas.import_assignments(self.id)
			self.data['students'] = self.canvas.import_students(self.id)
			self.data['missing'] = dict()

			for student_id in self.data['students']:
				if not student_id in self.data['missing']:
					self.data['missing'][student_id] = dict()

			for assignment_id in self.data['assignments']:
				self.get_missing(assignment_id)
			
			cfg.save(self.data, config_file = self.data_file)

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
	
	#def toggle_missing(self,assignment_id,student_id):
	#	self.data['missing'][student_id][assignment_id] = not self.data['missing'][student_id][assignment_id]


if __name__ == '__main__':
	dotenv.load_dotenv()
	URL = os.getenv('CANVAS_API_URL')
	KEY = os.getenv('CANVAS_API_KEY')
	COURSE_ID = 805953
	COURSE_NAME = 'Necromancy'
	printer = miaprinter.MiaPrinter()
	importer = test_import.TestImporter()
	#importer = canvasimport.CanvasImporter(URL, KEY)
	course = Course(COURSE_ID, COURSE_NAME,printer,importer)
	data = course.preview()
	course.print_report(data)