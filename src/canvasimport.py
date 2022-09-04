import canvasapi, dotenv, os

class CanvasImporter(canvasapi.Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def import_courses(self):
		courses = self.get_courses(
			enrollment_type = 'teacher',
			enrollment_state = 'active'
		)
		course_dict = {}
		for course in courses:
			course_dict[course.id] = course.name
		return course_dict
	
	def import_students(self, course_id):
		course = self.get_course(course_id)
		users = course.get_users(enrollment_type=['student'])
		user_dict = {}
		for user in users:
			user_dict[user.id] = user.sortable_name
		user_dict[1252174] = 'Student, Test'
		return user_dict
	
	def import_assignments(self, course_id):
		course = self.get_course(course_id)
		assignments = course.get_assignments()
		assign_dict = {}
		for assignment in assignments:
			assign_dict[assignment.id] = {
				'name':assignment.name,
				'points':assignment.points_possible,
				'due':assignment.due_at
			}
		return assign_dict
	
	def import_submissions(self, course_id, assignment_id):
		course = self.get_course(course_id)
		assignment = course.get_assignment(assignment_id)
		#sections = course.get_sections()
		#for section in sections:
		submissions = assignment.get_submissions(
			include = ['user']
		)
		submission_dict = {}
		for submission in submissions:
			submission_dict[submission.user['id']] = submission.missing
		return submission_dict



	#Functions below this line are deprecated

	def get_missing(self, course_id, showtest=False):
		course = self.get_course(course_id)
		sections = course.get_sections()
		for section in sections:
			enrollment_type = ['StudentEnrollment']
			if showtest:
					enrollment_type.append('StudentViewEnrollment')
			enrollments = section.get_enrollments(state='active', type=enrollment_type)
			data = dict()
			for enrollment in enrollments:
				results = self.process_user(enrollment, section)
				data[results[0]] = results[1]
		return data

	def process_user(self, enrollment, section):
		missing_submissions = self.get_user_missing(section=section, user_id=enrollment.user['id'])
		return [
			enrollment.user['sortable_name'],
			missing_submissions
		]

	def get_user_missing(self, section, user_id):
		submissions = section.get_multiple_submissions(
			student_ids=[user_id],
			include=['assignment'],
			workflow_state='unsubmitted'
		)
		missing_list = []
		for item in submissions:
			if item.missing:
				item_data = {
					'name':item.assignment['name'],
					'points':item.assignment['points_possible'],
					'due':self.format_date(item.assignment['due_at']),
				}
				missing_list.append(item_data)
		return missing_list

	def format_date(self, date):
		months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
		day,time = date.split('T')
		year,month,day = day.split('-')
		month = months[month]
		return ' '.join([day,month,year])



if __name__ == '__main__':
	dotenv.load_dotenv()
	URL = os.getenv('CANVAS_API_URL')
	KEY = os.getenv('CANVAS_API_KEY')
	canvas = CanvasImporter(URL, KEY)
	#USER_ID = 1252154
	#ASSIGNMENT_ID = 4100760
	#COURSE_ID = 805953
	#assignments = canvas.get_assignments(COURSE_ID)
	#users = canvas.get_students(COURSE_ID)
	#print(users)
	#assignment_ids = [key for key in assignments]
	#print(assignments)
	#course = canvas.get_course(COURSE_ID)
	#enrollments = course.get_enrollments()
	#for enrollment in enrollments:
	#	print(enrollment.user['id'],enrollment.user['name'])

	#for key,item in canvas.get_submissions(COURSE_ID,ASSIGNMENT_ID).items():
	#	print(users[key], item)