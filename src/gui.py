import tkinter as tk
from tkinter import ttk
import dotenv, os, miaprinter, canvasimport, app as a
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
		ttk.Button(mainframe, text='Preview', command=self.preview).grid(
			column=1, row=2, sticky=(tk.E, tk.W))

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
	
	def preview(self):
		popup = tk.Toplevel()
		popup.grab_set()

		idx = self.lbox.curselection()[0]
		course_id = self.course_ids[idx]
		self.data = self.app.get_data(course_id)

		row = 0
		for student_id, student_name in self.data['students'].items():
			ttk.Label(popup,text=student_name).grid(row=row,column=0,sticky=(tk.W))
			row += 1
			for assignment_id, assignment in self.data['assignments'].items():
				if self.data['missing'][student_id][assignment_id]:
					self.data['missing'][student_id][assignment_id] = tk.BooleanVar(
						value = self.data['missing'][student_id][assignment_id])
					ttk.Checkbutton(
						popup,
						text = assignment['name'],
						variable = self.data['missing'][student_id][assignment_id]
					).grid(row=row,column=0,sticky=(tk.W))
					row += 1
		
		ttk.Button(popup,text='Save and Print',command=lambda: self.print_report(popup)).grid(
			row=0,column=1,sticky = (tk.N, tk.E)
		)

	def print_report(self,popup):
		popup.destroy()
		for key in self.data['missing']:
			for item in self.data['missing'][key]:
				if type(self.data['missing'][key][item]) != bool:
					self.data['missing'][key][item] = bool(self.data['missing'][key][item].get())
		self.app.print_report(self.data)

if __name__ == '__main__':
	#dotenv.load_dotenv()
	#URL = os.getenv('CANVAS_API_URL')
	#KEY = os.getenv('CANVAS_API_KEY')
	printer = miaprinter.MiaPrinter()
	#canvas = canvasimport.CanvasImporter(URL, KEY)
	canvas = test_import.TestImporter()
	app = a.App(importer = canvas, printer = printer)
	gui = GUI(app)
	gui.mainloop()