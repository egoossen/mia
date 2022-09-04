import random, ekgconfig

class TestImporter():
	def __init__(self):
		self.cfg = dict()
		self.cfg = ekgconfig.load(config_file='test-config.json')
	
	def import_courses(self):
		return self.cfg['courses']

	def import_students(self, course_id):
		return self.cfg['students']

	def import_assignments(self, course_id):
		return self.cfg['assignments']
		
	def import_submissions(self, course_id, assignment_id):
		submission_dict = {}
		for student_id in self.cfg['students']:
			submission_dict[student_id] = self.cfg['missing'][student_id][assignment_id]
		return submission_dict

	def generate_random_missing(self):
		for assignment_id in self.cfg['assignments']:
			is_missing = random.choices([True,False], k=(len(self.cfg['students'])))
			i=0
			for student_id in self.cfg['students']:
				self.cfg['missing'][student_id][assignment_id] = is_missing[i]
				i += 1

if __name__ == '__main__':
	importer = TestImporter()
	print(importer.import_submissions(1, '76535'))