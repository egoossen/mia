import tkinter as tk
from tkinter import ttk
import dotenv, os, miaprinter, canvasimport, app as a, scrollableframe as sf
import test_import


class GUI(tk.Tk):
	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app

		self.title('MIA')
		mainframe = ttk.Frame(self, padding='3 3 12 12')
		mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.coursevar = tk.StringVar()

		ttk.Label(mainframe, text='Select one or more courses:').grid(
			column=0, row=0, sticky=(tk.N, tk.W))
		self.lbox = tk.Listbox(mainframe,
			listvariable=self.coursevar,
			selectmode='browse',
			height=10
		)
		self.lbox.grid(column=0, row=1, rowspan=2, sticky=(tk.N, tk.W))

		ttk.Button(mainframe, text='Reload Courses', command=self.update_courses).grid(
			column=1, row=1, sticky=(tk.E, tk.W))
		pb = ttk.Button(mainframe, text='Preview', command=self.preview)
		pb.grid(column=1, row=2, sticky=(tk.E, tk.W))
		pb.state(['disabled'])
		self.lbox.bind('<<ListboxSelect>>', lambda e: pb.state(['!disabled']))
		self.lbox.bind('<Double-1>', lambda e: self.preview())

		for child in mainframe.winfo_children():
			child.grid_configure(padx=5, pady=5)

		self.load_courses()

	def load_courses(self):
		self.course_ids = [key for key in self.app.cfg['courses']]
		self.courses = [self.app.cfg['courses'][key] for key in self.course_ids]
		self.coursevar.set(self.courses)
		for i in range(0, len(self.courses), 2):
			self.lbox.itemconfigure(i, background='#f0f0ff')
	
	def update_courses(self):
		self.app.import_courses()
		self.load_courses()
	
	def new_assignments(self,new_assignments):
		popup = tk.Toplevel()
		popup.wait_visibility()
		popup.grab_set()
		popup.title('Add New Assignments')
		frame = ttk.Frame(popup, padding='5')
		frame.grid(row=1,column=0,columnspan=2,sticky=(tk.N, tk.E, tk.S, tk.W))
		label_text = '{} new assignments found! Press "Save"\nto include selected assignments.'.format(len(new_assignments))
		ttk.Label(popup,text=label_text).grid(
			row=0,column=0,columnspan=2,sticky=(tk.E, tk.W))
		include_assignment = {}
		row = 0
		for assignment_id, assignment in new_assignments.items():
			include_assignment[assignment_id] = tk.BooleanVar(value=True)
			ttk.Checkbutton(
				frame,
				text = assignment['name'],
				variable = include_assignment[assignment_id]
			).grid(row=row,column=0,sticky=(tk.W))
			row += 1
		ttk.Button(
			popup,
			text='Save',
			command=lambda:self.add_assignments(include_assignment,popup)
		).grid(row=2,column=1)
		ttk.Button(popup,text='Close',command=popup.destroy).grid(row=2, column=0)
		
		for child in popup.winfo_children():
			child.grid_configure(padx=5, pady=5)
		
		popup.wait_window()
	
	def add_assignments(self,include_assignment,popup):
		for key in include_assignment:
			include_assignment[key] = bool(include_assignment[key].get())
		self.app.add_assignments(include_assignment)
		popup.destroy()
	
	def preview(self):
		idx = self.lbox.curselection()[0]
		course_id = self.course_ids[idx]

		title_str = self.courses[idx] + ' Report Preview'

		new_assignments = self.app.initialize_course(course_id)
		if (len(new_assignments)) != 0:
			self.new_assignments(new_assignments)

		self.data = self.app.get_data()

		popup = tk.Toplevel()
		popup.wait_visibility()
		popup.grab_set()
		popup.title(title_str)
		missing_fr = sf.ScrollableFrame(popup,width=350,height=350,padding='5')
		missing_fr.grid(row=0,column=1,sticky=(tk.N, tk.E, tk.S, tk.W))

		row = 0
		student_labels = {}

		for student_id, student_name in self.data['students'].items():
			student_included = False
			student_labels[student_id] = ttk.Label(
				missing_fr.scrollable_frame,
				text=student_name
			)
			for assignment_id, assignment in self.data['assignments'].items():
				if self.data['missing'][student_id][assignment_id]:
					if not student_included:
						student_labels[student_id].grid(row=row,column=0,sticky=(tk.W))
						row += 1
						student_included = True
					include_student = True
					self.data['missing'][student_id][assignment_id] = tk.BooleanVar(
						value = self.data['missing'][student_id][assignment_id])
					ttk.Checkbutton(
						missing_fr.scrollable_frame,
						text = assignment['name'],
						variable = self.data['missing'][student_id][assignment_id]
					).grid(row=row,column=0,sticky=(tk.W))
					row += 1

		
		ttk.Button(popup,text='Save and Print',command=lambda: self.print_report(popup)).grid(
			row=0,column=2,sticky = (tk.E, tk.W)
		)
		for child in popup.winfo_children():
			child.grid_configure(padx=5, pady=5)

	def print_report(self,popup):
		popup.destroy()
		for key in self.data['missing']:
			for item in self.data['missing'][key]:
				if type(self.data['missing'][key][item]) != bool:
					self.data['missing'][key][item] = bool(self.data['missing'][key][item].get())
		self.app.print_report(self.data)

if __name__ == '__main__':
	dotenv.load_dotenv()
	URL = os.getenv('CANVAS_API_URL')
	KEY = os.getenv('CANVAS_API_KEY')
	printer = miaprinter.MiaPrinter()
	canvas = canvasimport.CanvasImporter(URL, KEY)
	#canvas = test_import.TestImporter()
	app = a.App(importer = canvas, printer = printer)
	gui = GUI(app)
	gui.mainloop()