from canvasapi import Canvas

class CanvasImporter(Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

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

	def import_courses(self):
		courses = self.get_courses(
			enrollment_type = 'teacher',
			enrollment_state = 'active'
		)
		course_dict = {}
		for course in courses:
			course_dict[course.id] = course.name
		return course_dict
