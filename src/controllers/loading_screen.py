import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class LoadingScreenController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)
        self.progress = ttk.Progressbar(self.frame, mode='indeterminate', style='info.TProgressbar')
        self.progress.pack(pady=20)
        self.label = ttk.Label(self.frame, text="Loading...", font=("Helvetica", 16))
        self.label.pack(expand=True)

    def show(self):
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        self.progress.start()

    def hide(self):
        self.progress.stop()
        self.frame.place_forget()
