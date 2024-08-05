import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class LoadingScreenController:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.frame)
        self.label = ttk.Label(self.frame, text="Loading...", font=("Helvetica", 24))
        self.label.pack(expand=True)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()
