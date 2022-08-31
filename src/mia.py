from tkinter import *
from tkinter import ttk
import dotenv, subprocess, os, platform, errno, webbrowser
import json, canvasimport, miaprinter, sys

class MIA(Tk):
	def __init__(self, canvas, printer, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.canvas = canvas
		self.printer = printer

		self.title('MIA')
		mainframe = ttk.Frame(self,padding='3 3 12 12')
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.load_cfg()
		self.coursesvar = StringVar()

		ttk.Label(mainframe, text='Select one or more courses:').grid(
			column=0, row=0, sticky=(N, W))
		self.lbox = Listbox(mainframe, listvariable=self.coursesvar, selectmode='extended', height=10)
		self.lbox.grid(column=0, row=1, rowspan=2, sticky=(N, W))

		ttk.Button(mainframe, text='Reload Courses', command=self.update_courses).grid(
			column=1, row=1, sticky=(E, W))
		ttk.Button(mainframe, text='Generate', command=self.generate).grid(
			column=1, row=2, sticky=(E, W))

		for child in mainframe.winfo_children():
			child.grid_configure(padx=5, pady=5)

		self.load_courses()

	def load_courses(self):
		self.course_ids = [key for key in self.cfg['mycourses']]
		self.courses = [self.cfg['mycourses'][key] for key in self.course_ids]
		self.coursesvar.set(self.courses)
		for i in range(0, len(self.courses), 2):
			self.lbox.itemconfigure(i, background='#f0f0ff')

	def generate(self):
		#html_txt = '''
		#<html>
		#<p>Hello World!</p>
		#</html>
		#'''
		#with open('test.html','w') as f:
		#	f.write(html_txt)
		#print('Generating report...')
		#webbrowser.open('test.html')
		#return
		course_ids = [self.course_ids[idx] for idx in self.lbox.curselection()]
		for course_id in course_ids:
			course_name = self.courses[self.course_ids.index(course_id)]
			data = self.canvas.get_missing(course_id,showtest=self.cfg['showtest'])
			outfile = course_name.replace(' ','-') + '-mia-report.html'
			html_file = self.printer.dict2html(course_name, data)
			with open(outfile, 'w') as f:
				f.write(html_file)
			#webbrowser.open('template.html')
			webbrowser.open(outfile)
			#self.printer.dict2pdf(course_name, data, outfile)
			#self.open_file(outfile)

	def open_file(self, filepath):
		if getattr(sys, 'frozen', False):
			file_dir = sys._MEIPASS
		else:
			file_dir = ''
		filepath = file_dir + filepath
		if platform.system() == 'Darwin':		# macOS
			subprocess.call(('open', filepath))
		elif platform.system() == 'Windows':		# Windows
			os.startfile(filepath)
		else:						# linux variants
			subprocess.call(('xdg-open', filepath))

	def update_courses(self):
		#print('Updating courses...')
		course_dict = self.canvas.import_courses()
		self.cfg['mycourses'] = course_dict
		self.save_cfg()
		self.load_courses()

	def load_cfg(self):
		try:
			with open('config.json') as json_data_file:
				self.cfg = json.load(json_data_file)
		except FileNotFoundError:
			self.cfg = {'showtest':False,'mycourses':dict()}
			self.save_cfg()

	def save_cfg(self):
		with open('config.json', 'w') as outfile:
			json.dump(self.cfg, outfile)

def print_dict(my_dict):
	for key,value in my_dict.items():
		print (key,':',value)

if __name__ == '__main__':
	#if not os.path.exists('../env.json'):
	#	print ('User access key missing, please configure .env file')
	#	raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), '.env')
	dotenv.load_dotenv()
	URL = os.getenv('CANVAS_API_URL')
	KEY = os.getenv('CANVAS_API_KEY')
	#print(os.listdir())
	#with open('test.json') as env_file:
	#	ENV = json.load(env_file)
	#	URL = ENV['CANVAS_API_URL']
	#	KEY = ENV['CANVAS_API_KEY']
	printer = miaprinter.MiaPrinter()
	canvas = canvasimport.CanvasImporter(URL, KEY)
	app = MIA(canvas,printer)
	app.mainloop()

