import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
	def __init__(self, container, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		canvas = tk.Canvas(self)
		scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
		self.scrollable_frame = ttk.Frame(canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(
				scrollregion=canvas.bbox("all")
			)
		)

		canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

		canvas.configure(yscrollcommand=scrollbar.set)

		canvas.grid(row=0,column=0,sticky=(tk.N,tk.E,tk.W,tk.S))
		scrollbar.grid(row=0,column=1,sticky=(tk.N,tk.S))
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0,weight=1)
